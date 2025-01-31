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

    blog_post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='leaky_bucket')
    bucket_size = models.IntegerField(default=0)
    bucket_capacity = models.IntegerField(default=500)
    leak_rate = models.IntegerField(default=100)
    last_record = models.FloatField()
