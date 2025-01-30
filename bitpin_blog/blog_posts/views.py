from django.shortcuts import redirect, render
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BlogPostSerializer

class BlogPostCreateView(APIView):
    """This view creates blog posts based on authenticated user requests."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Will handle blog post creation."""

        serializer = BlogPostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(author=request.user)
        return redirect('/')

    def get(self, request):
        """Will respond with the blog post form page."""

        return render(request, 'blog_post_create.html')
