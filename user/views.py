from django.shortcuts import render
from .models import CustomUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import login,authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from serializers import *

# Create your views here.
class Login(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            hashed_pass = make_password(serializer.validated_data['password'])
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email)
            if not user:
                return Response({'message':'You are not registered.'})
            
            if not user.check_password(hashed_pass):
                return Response({'message':'Something went wrong. Try again later.'})
            
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response(
                {
                    "message": "Login successful",
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)