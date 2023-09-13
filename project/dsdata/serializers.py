
from rest_framework import serializers
from .models import SensorData


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'


class SensorUploadSerializer(serializers.Serializer):
    sensors = serializers.CharField(max_length=10000)
