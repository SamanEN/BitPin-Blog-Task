from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RateSerializer

class RateCreateView(APIView):
    """This view will only handle creating ratings for blogs."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            blog_id = request.data.get('blog')
            return redirect(f'/blog/{blog_id}')
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
