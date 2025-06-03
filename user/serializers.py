from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from drf_spectacular.utils import extend_schema_field
User = get_user_model() 


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150,required=True,)
    password = serializers.CharField(
           write_only=True,
           required=True,
           style={'input_type': 'password', 'placeholder': 'Password'}
       )