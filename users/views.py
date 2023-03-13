from django.conf import settings
from django.contrib.auth.models import User, BaseUserManager

from google.auth.transport import requests
from google.oauth2 import id_token

from rest_framework import permissions, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class BlackListTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(data={"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthenticate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        auth_token = request.data["auth_token"]
        client_id = settings.GOOGLE_CLIENT_ID
        id_info = id_token.verify_oauth2_token(auth_token, requests.Request())
        if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise exceptions.AuthenticationFailed("The token is either invalid or has expired")
        if id_info["aud"] != client_id:
            raise exceptions.AuthenticationFailed("Authentication Failed")
        try:
            user = User.objects.get(email=id_info["email"])
        except User.DoesNotExist:
            user_data = {
                "username": id_info["email"], # unique constraint for username
                "email": id_info["email"],
                "password": BaseUserManager().make_random_password(),
                "first_name": "sdfsf",
                "last_name": "sdfdsf"
            }
            user_serializer = RegisterSerializer(data=user_data)
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
