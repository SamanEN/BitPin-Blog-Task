from django.urls import path
from .views import BlogPostCreateView, BlogPostsListView, BlogPostDisplayView

urlpatterns = [
    path("create/", BlogPostCreateView.as_view(), name='create_blog_post'),
    path("", BlogPostsListView.as_view(), name='blog_posts_list'),
    path("<int:blog_id>/", BlogPostDisplayView.as_view(), name='blog_post_display')
]
