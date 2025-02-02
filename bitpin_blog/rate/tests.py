from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker

from blog_posts.models import BlogRatingLeakyBucket

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


    def test_user_rating_limiter(self):
        """
        This test will send as many requests as the bucket capacity, under one
        second to get `too many requests` response.
        """

        url = reverse('rate_blog')
        rate = {
            'blog': self.blog_post_id,
            'rating': 1
        }

        for user in self.users[:-1]:
            self.authenticate_user(user)
            response = self.client.post(url, rate)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        last_user = self.users[len(self.users) - 1]
        self.authenticate_user(last_user)
        response = self.client.post(url, rate)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
