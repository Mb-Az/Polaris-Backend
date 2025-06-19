from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

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
        fields = ['password','name']  # add other fields as needed
    def create(self, request):
        id = create_short_uuid4()
        return MobileDevice.objects.create(id=id, name=request['name'])
    
class LoginSerializer(serializers.Serializer):
    mobile_id = serializers.CharField()
    # password = serializers.CharField(write_only=True)