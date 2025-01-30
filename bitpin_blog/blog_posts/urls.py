from django.urls import path
from .views import BlogPostCreateView

urlpatterns = [
    path("create/", BlogPostCreateView.as_view())
]
