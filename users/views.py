from django.conf import settings
from django.contrib.auth.models import User, BaseUserManager

from google.auth.transport import requests
from google.oauth2 import id_token

import hashlib

import requests as default_requests

from rest_framework import permissions, status, exceptions
from rest_framework.views import APIView
from rest_framework.utils import json
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

import unicodedata

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

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_email(id):
    return "f"+str(id)+"@fba.com"

def generate_username(first_name, last_name, id):
    first_name = remove_accents(first_name.lower())
    last_name = remove_accents(last_name.lower())
    unique_str = hashlib.sha1(id.encode("UTF-8")).hexdigest()
    unique_str = unique_str[:8]
    return first_name+'.'+last_name+'.'+unique_str


class FacebookAuthenticate(APIView):
    def get(self, request):
        # https://facebook.com/dialog/oauth?client_id=236109032265868&redirect_uri=http://localhost:8000/users/facebook-authen/

        # get users access token from code in the facebook login dialog redirect
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={your-facebook-apps-id}&redirect_uri=http://localhost:8000/users/facebook-authen/&client_secret={app_secret}&code={code-generated-from-login-result}
        user_access_token_payload = {
            "client_id": settings.FACEBOOK_APP_ID,
            "redirect_uri": "http://localhost:8000/users/facebook-authen/",
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "code": request.query_params.get("code"),
        }
        user_access_token_request = default_requests.get(
            settings.FACEBOOK_ACCESS_TOKEN_URL, params=user_access_token_payload
        )
        user_access_token_response = json.loads(user_access_token_request.text)
        print("user access token: ",user_access_token_response)
        if "error" in user_access_token_response:
            user_access_token_error = {
                "message": "Wrong Facebook access token / This Facebook access token is already expired."
            }
            return Response(user_access_token_error)
        user_access_token = user_access_token_response["access_token"]

        # get developers access token
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={your-app-id}&client_secret={your-app-secret}&grant_type=client_credentials
        developers_access_token_payload = {
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "grant_type": "client_credentials",
        }
        developers_access_token_request = default_requests.get(
            settings.FACEBOOK_ACCESS_TOKEN_URL, params=developers_access_token_payload
        )
        developers_access_token_response = json.loads(
            developers_access_token_request.text
        )
        if "error" in developers_access_token_response:
            developers_access_token_error = {
                "message": "Invalid request for access token."
            }
            return Response(developers_access_token_error)
        developers_access_token = developers_access_token_response["access_token"]

        # inspect the users access token --> validate to make sure its still valid
        # https://graph.facebook.com/debug_token?input_token={token-to-inspect}&access_token={app-token-or-admin-token}
        # Get user ID
        verify_user_access_token_payload = {
            "input_token": user_access_token,
            "access_token": developers_access_token,
        }
        verify_user_access_token_request = default_requests.get(
            settings.FACEBOOK_DEBUG_TOKEN_URL, params=verify_user_access_token_payload
        )
        verify_user_access_token_response = json.loads(
            verify_user_access_token_request.text
        )
        if "error" in verify_user_access_token_response:
            verify_user_access_token_error = {
                "message": "Could not verifying user access token."
            }
            return Response(verify_user_access_token_error)
        user_id = verify_user_access_token_response["data"]["user_id"]

        # get user's email
        # https://graph.facebook.com/{your-user-id}?fields=id,name,email&access_token={your-user-access-token}
        user_info_url = settings.FACEBOOK_URL + user_id
        user_info_payload = {
            "fields": "id,name,first_name, last_name, middle_name, picture",
            "access_token": user_access_token,
        }
        user_info_request = default_requests.get(user_info_url, params=user_info_payload)
        user_info_response = json.loads(user_info_request.text)
        print("user info:", user_info_response)
        # users_email = user_info_response["email"]
        fba_email = generate_email(user_info_response["id"])
        fba_username = generate_username(user_info_response["first_name"],user_info_response["last_name"], user_info_response["id"] )
        # create user if not exist
        try:
            user = User.objects.get(email=fba_email)
        except User.DoesNotExist:
            user_data = {
                    "username": fba_username, # unique constraint for username
                    "email": fba_email,
                    "password": BaseUserManager().make_random_password(),
                    "first_name": user_info_response["first_name"],
                    "last_name": user_info_response["last_name"],
            }
            user_serializer = RegisterSerializer(data=user_data)
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
            user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)