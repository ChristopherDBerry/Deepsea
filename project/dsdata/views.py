import csv
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import SensorData
from .serializers import SensorDataSerializer, SensorUploadSerializer


class SensorDataNormalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SensorDataViewSet(viewsets.ModelViewSet):
    """
    API endpoints for sensor data
    """
    queryset = SensorData.objects.all().order_by('-id')
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        limit = self.request.query_params.get('limit')
        if not limit:
            return SensorData.objects.all()
        limit = int(limit)
        return SensorData.objects.all()[:limit]


@method_decorator(csrf_exempt, name='dispatch')  # No auth for demo
class SensorDataUploadView(APIView):
    serializer_class = SensorUploadSerializer

    def normalize_field(self, field, field_name):
        """ handle missing fields and outliers"""
        field = float(field) if field != '' else None
        # missing
        if field is None:
            if not self.regression_data:
                raise SensorDataNormalizationError(
                    f"Not enough data to normalize {field_name}")
            # Use linear regression to predict the missing value
            timestamps = [x.datetime.timestamp()
                          for x in self.regression_data]
            points = [getattr(x, f"{field_name}_normalized")
                      for x in self.regression_data]
            # Convert the target timestamp to a timestamp value
            target_timestamp_value = self.now.timestamp()
            regression = LinearRegression()
            regression.fit(np.array(timestamps).reshape(-1, 1), points)
            predicted = regression.predict(
                np.array([[target_timestamp_value]]))[0]
            return (field, predicted)

        # outlier
        return (field, None)

    def post(self, request, format=None):
        serializer = SensorUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        csv_line = request.data.get('sensors', None)

        # Cache here to avoid multiple queries
        self.regression_data = SensorData.objects.all()[:20]

        csv_data = csv.reader([csv_line])
        row = next(csv_data)
        del row[0]

        if len(row) != 12:
            return Response({'error': "Invalid number of fields"},
                            status=status.HTTP_400_BAD_REQUEST)

        self.now = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        try:
            (latitude, latitude_correction
                ) = self.normalize_field(row[0], 'latitude')
            (longitude, longitude_correction
                ) = self.normalize_field(row[1], 'longitude')
            (speed_overground, speed_overground_correction
                ) = self.normalize_field(row[3], 'speed_overground')
            (stw, stw_correction
                ) = self.normalize_field(row[4], 'stw')
            (direction, direction_correction
                ) = self.normalize_field(row[5], 'direction')
            (current_ucomp, current_ucomp_correction
                ) = self.normalize_field(row[6], 'current_ucomp')
            (current_vcomp, current_vcomp_correction
                ) = self.normalize_field(row[7], 'current_vcomp')
            (draft_aft, draft_aft_correction
                ) = self.normalize_field(row[8], 'draft_aft')
            (draft_fore, draft_fore_correction
                ) = self.normalize_field(row[9], 'draft_fore')
            (comb_wind_swell_wave_height,
                comb_wind_swell_wave_height_correction
                    ) = self.normalize_field(row[10], 'comb_wind_swell_wave_height')
            (power, power_correction
                ) = self.normalize_field(row[11], 'power')
        except SensorDataNormalizationError as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        sensor_data = SensorData(
            datetime=self.now,
            latitude=latitude,
            latitude_correction=latitude_correction,
            longitude=longitude,
            longitude_correction=longitude_correction,
            speed_overground=speed_overground,
            speed_overground_correction=speed_overground_correction,
            stw=stw,
            stw_correction=stw_correction,
            direction=direction,
            direction_correction=direction_correction,
            current_ucomp=current_ucomp,
            current_ucomp_correction=current_ucomp_correction,
            current_vcomp=current_vcomp,
            current_vcomp_correction=current_vcomp_correction,
            draft_aft=draft_aft,
            draft_aft_correction=draft_aft_correction,
            draft_fore=draft_fore,
            draft_fore_correction=draft_fore_correction,
            comb_wind_swell_wave_height=comb_wind_swell_wave_height,
            comb_wind_swell_wave_height_correction=(
                comb_wind_swell_wave_height_correction),
            power=power,
            power_correction=power_correction,
        )
        sensor_data.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

