from django.urls import path
from .views import RateCreateView, BlogRatingStatsView

urlpatterns = [
    path("", RateCreateView.as_view(), name='rate_blog'),
    path("get/<int:blog_id>/", BlogRatingStatsView.as_view(), name='blog_rating_stats')
]
