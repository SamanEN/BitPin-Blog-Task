from django.urls import path
from .views import BlogPostCreateView, BlogPostsListView

urlpatterns = [
    path("create/", BlogPostCreateView.as_view(), name='create_blog_post'),
    path("", BlogPostsListView.as_view(), name='blog_posts_list')
]
