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

    def save(self, *args, **kwargs):
        """Overrides the default save method to update the blog average rating
        when the instance is first created."""

        if self.pk is None:
            blog_ratings_count = Rate.objects.filter(blog=self.blog).count()
            current_average_rating = self.blog.average_rating
            updated_rating = \
                (current_average_rating * blog_ratings_count + self.rating) / (blog_ratings_count + 1)
            self.blog.average_rating = updated_rating
            self.blog.save()
        
        super().save(*args, **kwargs)