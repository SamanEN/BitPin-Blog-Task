import time
import math

from blog_posts.models import BlogPost, BlogRatingEma, BlogRatingLeakyBucket
from .models import Rate

def can_request_rating_leaky_bucket(blog_post: BlogPost) -> bool:
    """
    Whenever a new rating comes, the associated leaky bucket of the related blog
    post should be updated. This function will take the blog post and update its
    bucket accordingly.

    Return: A boolean indicating whether the current rating should be accepted
    or discarded.
    """

    bucket: BlogRatingLeakyBucket = blog_post.leaky_bucket
    
    elapsed_time = int(time.time()) - bucket.last_record
    bucket.last_record = time.time()

    bucket.bucket_size -= elapsed_time * bucket.leak_rate
    bucket.bucket_size = max(bucket.bucket_size, 0)

    bucket.bucket_size += 1

    if bucket.bucket_size > bucket.bucket_capacity:
        bucket.bucket_size = bucket.bucket_capacity
        bucket.save()
        return False
    
    bucket.save()
    return True

def can_request_rating_ema(blog_post: BlogPost) -> bool:
    """
    This function updates the exponential moving average model sequentially. It
    then checks the current state against the threshold defined as a global
    constant to check if the current request rate is acceptable or not.
    """

    ratings_count = Rate.objects.filter(blog_post=blog_post).count()
    ema = BlogRatingEma.objects.get(blog_post=blog_post)

    current_rate = time.time() - ema.last_record
    ema.last_record = time.time()

    current_mean = ema.mean_request_rate
    updated_mean = (current_mean + current_rate) / (ratings_count + 1)

    current_variation_sum = ema.variation_sum
    updated_variation_sum = current_variation_sum + (current_rate - updated_mean) ** 2
    std = math.sqrt(updated_variation_sum / (ratings_count + 1))
    std = 1 if std == 0 else std

    z = (current_rate - updated_mean) / std

    ema.mean_request_rate = updated_mean
    ema.variation_sum = updated_variation_sum
    ema.save()

    if ratings_count == 0:
        return True
    return z > BlogRatingEma.THRESHOLD