from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import BlogPost
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
    
class BlogPostsListView(APIView):
    """This view will simply return the list of all blogs created by users."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        blog_posts = BlogPost.objects.all()
        return render(request, 'blogs_list.html', {'blog_posts': blog_posts})
    
class BlogPostDisplayView(APIView):
    """This view will return and display a specified blog post."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, blog_id):
        """Will fetch a blog post and display it to the user."""

        blog = get_object_or_404(BlogPost, id=blog_id)
        return render(request, 'blog_post.html', {'blog': blog})
