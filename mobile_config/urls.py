from django.urls import path
from .views import SetConfigurationView, GetConfigurationView

urlpatterns = [
    path('set/', SetConfigurationView.as_view(), name='set-config'),
    path('get/', GetConfigurationView.as_view(), name='get-config'),
]
