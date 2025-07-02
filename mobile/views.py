from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from hashlib import sha256

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import *
from .serializers import *
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from polaris_back.settings import MOBILE_DEVICE_REGISTER_PASS

# Create your views here.
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile_id = serializer.validated_data['mobile_id']
            device = MobileDevice.objects.select_related('user').filter(id=mobile_id).first()
            if device is None or device.user.user_type != "device":
                return Response({'message': 'You are not registered.'}, status=400)
            
            refresh = RefreshToken.for_user(device.user) ###
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
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['password'] != MOBILE_DEVICE_REGISTER_PASS:
                return Response({'message':'You do not have the access.'})
            
            device = serializer.save()
            refresh = RefreshToken.for_user(device.user) ###
            access_token = refresh.access_token
            return Response(
                {
                    "message": "Login successful",
                    "id":str(device.id),
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckAuthView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        device = request.device
        return Response({"message":f"User logged in {device.id}"})
