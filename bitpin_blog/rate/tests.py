from django.http import HttpResponse
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from flags.state import flag_enabled
from faker import Faker
from freezegun import freeze_time
import datetime

from blog_posts.models import BlogRatingLeakyBucket


@freeze_time()
class RateLimiterAPITest(APITestCase):
    """
    Test the leaky bucket rate limiter with multiple users.
    """

    def setUp(self):
        """
        Creates multiple users and one blog post to rate it.
        """

        self.fake = Faker()

        self.users = []
        self.common_pass = 'test_users_123456'

        self.setup_create_first_post()
        self.blog_post_id = 1

        self.url = reverse('rate_blog')
        self.rate = {
            'blog': self.blog_post_id,
            'rating': 1
        }

        # As long as all the rating requests happen under one second, we'll need
        # rating requests as many as the bucket capacity. In this case bucket
        # won't leak and it wil get full under a second.
        users_count = BlogRatingLeakyBucket.BUCKET_CAPACITY + 1
        for i in range(users_count):
            username = f'user_{i + 1}'
            user = User.objects.create(
                username=username,
                email=self.fake.email(),
                password=self.common_pass
            )
            self.users.append(user)

        return super().setUp()

    def authenticate_user(self, user):
        """Logs in the user and returns the authentication session."""

        self.client.force_login(user)

    def setup_create_first_post(self):
        """A part of the setup to create a user and post the first blog."""

        author_user = User.objects.create(
            username='user_author',
            email='author@email.com',
            password='author_password'
        )
        self.authenticate_user(author_user)

        blog_post = {
            'title': self.fake.sentence(),
            'content': self.fake.paragraph()
        }

        url = reverse('create_blog_post')
        self.client.post(url, blog_post)

    @override_settings(
        FLAGS={
            'LEAKY_BUCKET': [('boolean', True)],
            'EMA': [('boolean', False)]
        }
    )
    def test_leaky_bucket(self):
        """
        This test will send as many requests as the bucket capacity, under one
        second to get `too many requests` response.
        """

        self.assertTrue(flag_enabled('LEAKY_BUCKET'))

        for user in self.users[:-1]:
            self.authenticate_user(user)
            response = self.client.post(self.url, self.rate)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        last_user = self.users[len(self.users) - 1]
        self.authenticate_user(last_user)
        response = self.client.post(self.url, self.rate)
        self.assertEqual(response.status_code,
                         status.HTTP_429_TOO_MANY_REQUESTS)

    @override_settings(
        FLAGS={
            'LEAKY_BUCKET': [('boolean', False)],
            'EMA': [('boolean', True)]
        }
    )
    def test_ema(self):
        """
        This test will first send few requests in fixed intervals and then send
        multiple requests in a bursty way to trigger the ema threshold.
        """

        self.assertTrue(flag_enabled('EMA'))
        self.assertFalse(flag_enabled('LEAKY_BUCKET'))

        normal_users = self.users[:15]
        bursty_users = self.users[15:]
        bursty_responses: list[HttpResponse] = []

        with freeze_time() as frozen_time:
            for user in normal_users:
                frozen_time.tick(datetime.timedelta(seconds=5))
                self.authenticate_user(user)
                response = self.client.post(self.url, self.rate)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            for user in bursty_users:
                frozen_time.tick(datetime.timedelta(milliseconds=50))
                self.authenticate_user(user)
                response = self.client.post(self.url, self.rate)
                bursty_responses.append(response)

        self.assertTrue(
            any(r.status_code ==
                status.HTTP_429_TOO_MANY_REQUESTS for r in bursty_responses),
            "No request exceeded rate limit."
        )
