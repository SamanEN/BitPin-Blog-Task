from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlogRatingLeakyBucket(models.Model):
    """
    This model saves the required information to implement the leaky algorithm
    over each blog post. This is to limit the rate at which rating requests are
    received.
    """

    BUCKET_CAPACITY = 20
    LEAK_RATE = 10

    blog_post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='leaky_bucket')
    bucket_size = models.IntegerField(default=0)
    bucket_capacity = models.IntegerField(default=BUCKET_CAPACITY)
    leak_rate = models.IntegerField(default=LEAK_RATE)
    last_record = models.IntegerField()

class BlogRatingEma(models.Model):
    """
    This model saves the required information to implement the Exponential
    moving average for rate limiting.
    """

    THRESHOLD = 2

    blog_post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='ema')
    mean_request_rate = models.FloatField(default=0)
    # To calculate the standard deviation sequentially
    variation_sum = models.FloatField(default=0)
    last_record = models.FloatField()
