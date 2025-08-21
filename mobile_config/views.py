from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Configuration
from .serializers import ConfigurationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SetConfigurationView(APIView):
    serializer_class = ConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only admins can update

    @swagger_auto_schema(
        request_body=ConfigurationSerializer,
        responses={200: ConfigurationSerializer},
        operation_description="Update or create system configuration from the frontend."
    )
    def post(self, request):
        config = Configuration.objects.first()
        serializer = self.serializer_class(instance=config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetConfigurationView(APIView):
    serializer_class = ConfigurationSerializer
    permission_classes = [permissions.AllowAny]  # Android can fetch without login

    @swagger_auto_schema(
        responses={200: ConfigurationSerializer},
        operation_description="Get current configuration for Android devices."
    )
    def get(self, request):
        config = Configuration.objects.first()
        if not config:
            config = Configuration.objects.create()  # Create default if none exist
        serializer = self.serializer_class(config)
        return Response(serializer.data, status=status.HTTP_200_OK)
