import time

from django.utils.timezone import now

from blog_posts.models import BlogPost, BlogRatingLeakyBucket

def can_request_rating(blog_post: BlogPost) -> bool:
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