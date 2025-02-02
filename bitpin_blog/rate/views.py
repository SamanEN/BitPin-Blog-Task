from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg, Count
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from blog_posts.models import BlogPost

from .serializers import RateSerializer
from .utils import can_request_rating
from .models import Rate
from .exceptions import BlogIsAlreadyRated, TooManyRatingRequests


class RateCreateView(APIView):
    """This view will only handle creating ratings for blogs."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RateSerializer(
            data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        blog = serializer.validated_data.get('blog')
        if Rate.objects.filter(user=request.user, blog=blog).exists():
            raise BlogIsAlreadyRated()

        if not can_request_rating(blog):
            raise TooManyRatingRequests()
        
        serializer.save(user=request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class BlogRatingStatsView(APIView):
    """This view will fetch displayed info of a blog post's ratings."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, blog_id):
        """
        Returns the average rating and the total number of ratings for a given blog post.
        """
        blog = get_object_or_404(BlogPost, id=blog_id)

        rating_data = Rate.objects.filter(blog=blog).aggregate(
            average_rating=Avg('rating'),
            total_ratings=Count('id')
        )

        return Response({
            "average_rating": rating_data["average_rating"] or 0,
            "total_ratings": rating_data["total_ratings"]
        }, status=status.HTTP_200_OK)


class UserRatingStatsView(APIView):
    """This view will fetch the current user rating for the specified blog."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, blog_id):
        rate = get_object_or_404(Rate, blog_id=blog_id, user=request.user)

        return Response({
            "user_rating": rate.rating
        },
            status=status.HTTP_200_OK
        )

class UpdateUserRatingView(APIView):
    """This view will update the rating of a blog for the current user."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        rate = get_object_or_404(Rate, user=request.user, blog_id=blog_id)
        
        serializer = RateSerializer(
            rate, data=request.data, context={'request': request}, partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return redirect('blog_post_display', blog_id=blog_id)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
