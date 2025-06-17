from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("check/", CheckAuthView.as_view(), name="check"),


]