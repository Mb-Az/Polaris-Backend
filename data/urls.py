from django.urls import path
from .views import AndroidDataUploadView, CellMeasurementListView, TestResultListView

urlpatterns = [
    path('android/upload/', AndroidDataUploadView.as_view(), name='android-upload'),
    path('cell-measurements/', CellMeasurementListView.as_view(), name='cell-measurements'),
    path('test-results/', TestResultListView.as_view(), name='test-results'),
]
