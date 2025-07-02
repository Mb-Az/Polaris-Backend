from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from user.models import CustomUser

from .models import MobileDevice
import os
import uuid
MOBILE_ID_LENGTH = 10
def create_short_uuid4():
    return uuid.uuid4().hex[:MOBILE_ID_LENGTH]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    class Meta:
        model = MobileDevice
        fields = ['password', 'name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        name = validated_data.pop('name')

        # Create the associated user
        user = CustomUser.objects.create_user(
            email=None,  
            password=None,  
            user_type="device",
            full_name=name,
        )

        user.set_unusable_password()
        user.save()

        device_id = create_short_uuid4()

        device = MobileDevice.objects.create(
            id=device_id,
            name=name,
            user=user
        )

        return device

    
class LoginSerializer(serializers.Serializer):
    mobile_id = serializers.CharField()
    # password = serializers.CharField(write_only=True)