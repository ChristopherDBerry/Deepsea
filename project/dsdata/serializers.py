
from rest_framework import serializers
from .models import SensorData


class SensorDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorData
        fields = [f.name for f in SensorData._meta.fields] + [
            'latitude_normalized',
            'longitude_normalized',
            'speed_overground_normalized',
            'stw_normalized',
            'direction_normalized',
            'current_ucomp_normalized',
            'current_vcomp_normalized',
            'draft_aft_normalized',
            'draft_fore_normalized',
            'comb_wind_swell_wave_height_normalized',
            'power_normalized',
            'sea_currents_speed_normalized',
            'sea_currents_angle_normalized',
        ]

    def __init__(self, *args, **kwargs):
        # Extract the 'limit' parameter from kwargs
        limit = kwargs.pop('limit', None)
        super(SensorDataSerializer, self).__init__(*args, **kwargs)

        # Modify the queryset based on the 'limit' parameter
        if limit is not None:
            self.Meta.model.objects = self.Meta.model.objects.all()[:limit]


class SensorUploadSerializer(serializers.Serializer):
    sensors = serializers.CharField(max_length=10000)
