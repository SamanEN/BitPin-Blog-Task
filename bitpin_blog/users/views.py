from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render

from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from .exceptions import UserIsRepetitive


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Will respond with the register page."""
        
        return render(request, 'register.html')

    def post(self, request):
        """Will handle user creation and signup form data."""

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=serializer.validated_data['username']).exists():
            raise UserIsRepetitive()

        user = serializer.save()

        login(request, user)

        return redirect('/')


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Will respond with the login page."""

        return render(request, 'login.html')

    def post(self, request):
        """Will handle user login data."""

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed()

        return redirect('/')
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout was successful.'}, status=status.HTTP_200_OK)
