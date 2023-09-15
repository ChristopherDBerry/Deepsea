from django.urls import path, include

from rest_framework import routers

from .views import SensorDataUploadView, SensorDataViewSet

router = routers.DefaultRouter()

router.register(
    r"sensor-data", SensorDataViewSet, basename="sensor-data")

urlpatterns = [
    path('', include(router.urls)),
    path('upload-sensor-data/', SensorDataUploadView.as_view(),
         name='upload-sensor-data'),
]
