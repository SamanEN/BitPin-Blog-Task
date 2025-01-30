from django.db import models
from django.contrib.auth.models import User
from blog_posts.models import BlogPost

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'blog'], name='unique_user_blog_rating')
        ]