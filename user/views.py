from django.shortcuts import render
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
from drf_yasg import openapi
from user.serializers import *
from user.models import *
from rest_framework.exceptions import ParseError
from .utils import create_short_uuid4 
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
        
            user = authenticate(request, email=email, password=password)
            if user is None:
                return Response({'message':'You are not registered.'},status=status.HTTP_401_BAD_REQUEST)

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
        
class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
        except ParseError:
             return Response({"error":"Wrong parameters format"},status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User registered successfully.",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CheckAuthView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({"message":f"User logged in {user.email}"})
class GetDeviceID(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
        
            user = authenticate(request, email=email, password=password)
            if user is None:
                return Response({'message':'You are not registered.'},status=status.HTTP_401_BAD_REQUEST)
            if user.user_type != "device":
                return Response({'message':'You are not authorized.'}, status=status.HTTP_403_BAD_REQUEST)
            
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            id_ = create_short_uuid4()
            device = Device.objects.create(
                id = id_
            )
            return Response(
                {
                    "message": "Device recognized successful",
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                    "Id" : str(id_)
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
