from django.urls import path
from .views import AndroidDataUploadView, DataListView

urlpatterns = [
    path('android/upload/', AndroidDataUploadView.as_view(), name='android-upload'),
    path('measurements/', DataListView.as_view(), name='data-fetch'),
]
