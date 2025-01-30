from django.urls import path
from .views import RateCreateView, BlogRatingStatsView, UserRatingStatsView

urlpatterns = [
    path("", RateCreateView.as_view(), name='rate_blog'),
    path("get_blog_rating/<int:blog_id>/", BlogRatingStatsView.as_view(), name='blog_rating_stats'),
    path("get_user_rating/<int:blog_id>/", UserRatingStatsView.as_view(), name='user_rating_stats'), 
]
