from rest_framework import serializers
from .models import Configuration

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = "__all__"
        read_only_fields = ["updated_by", "updated_at"]
