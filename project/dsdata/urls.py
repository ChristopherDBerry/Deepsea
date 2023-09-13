from django.contrib import admin
from django.urls import path
from .views import SensorDataUploadView

urlpatterns = [
    path('upload-sensor-data/', SensorDataUploadView.as_view(), name='upload-sensor-data'),
]