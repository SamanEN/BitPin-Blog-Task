from django.urls import path
from .views import RateCreateView

urlpatterns = [
    path("", RateCreateView.as_view(), name='rate_blog')
]
