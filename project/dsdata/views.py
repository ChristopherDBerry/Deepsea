import csv

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import SensorData
from .serializers import SensorDataSerializer, SensorUploadSerializer


@method_decorator(csrf_exempt, name='dispatch') # No authentication for this demo
class SensorDataUploadView(APIView):
    serializer_class = SensorUploadSerializer

    def post(self, request, format=None):
        serializer = SensorUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        csv_line = request.data.get('sensors', None)

        try:
            csv_data = csv.reader([csv_line])
            row = next(csv_data)
            del row[0]

            if len(row) != 12:
                raise Exception("Invalid number of fields")

            latitude = float(row[0])
            longitude = float(row[1])
            datetime = row[2]
            speed_overground = float(row[3])
            stw = float(row[4])
            direction = float(row[5])
            current_ucomp = float(row[6])
            current_vcomp = float(row[7])
            draft_aft = float(row[8])
            draft_fore = float(row[9])
            comb_wind_swell_wave_height = float(row[10])
            power = float(row[11])

            sensor_data = SensorData(
                latitude=latitude,
                longitude=longitude,
                datetime=datetime,
                speed_overground=speed_overground,
                stw=stw,
                direction=direction,
                current_ucomp=current_ucomp,
                current_vcomp=current_vcomp,
                draft_aft=draft_aft,
                draft_fore=draft_fore,
                comb_wind_swell_wave_height=comb_wind_swell_wave_height,
                power=power,
            )
            sensor_data.save()
        except Exception as e:
            return Response({'error': 'Invalid CSV data'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

