import csv
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SensorData
from .serializers import SensorDataSerializer, SensorUploadSerializer
from . import utils


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
    historic_length = 20

    def outlier_bands(self, field_name):
        """ Calculate outlier bands (modified Bollinger bands)
        for a specific field in the model. """
        if len(self.historic_data) < self.historic_length:
            raise SensorDataNormalizationError(
                f"Not enough data for outlier bands for {field_name}")
        # Skip if any of the very recent historic data is unreliable
        if (getattr(self.historic_data[0], f"{field_name}_correction") or
            getattr(self.historic_data[1], f"{field_name}_correction") or
                getattr(self.historic_data[2], f"{field_name}_correction")):
            raise SensorDataNormalizationError(
                f"Not enough reliable data for outlier bands for {field_name}")
        k = 5
        data = [getattr(x, f"{field_name}_normalized")
                for x in self.historic_data]
        # Calculate the moving average
        moving_average = sum(data) / len(data)
        # Calculate the moving standard deviation
        moving_std = (sum((x - moving_average) ** 2 for x in data
                          ) / (len(data) - 1)) ** 0.5
        # Increase k bassed on amount of _correction historical data,
        # eg higher tolerance for outliers if historic data is unreliable
        for i, row in enumerate(self.historic_data):
            bias = 10 * 0.9 ** i  # bias towards more recent unreliable data
            if getattr(row, f"{field_name}_correction") is not None:
                k += bias
        # Calculate the upper and lower bands
        upper_band = moving_average + k * moving_std
        lower_band = moving_average - k * moving_std
        return (upper_band, moving_average, lower_band)

    def predict_value(self, field_name):
        """ Predict the value of a field based on the historic data"""
        if not self.historic_data:
            raise SensorDataNormalizationError(
                f"Not enough data to predict missing {field_name}")
        # Use linear regression to predict the missing value
        timestamps = [x.datetime.timestamp()
                      for x in self.historic_data]
        points = [getattr(x, f"{field_name}_normalized")
                  for x in self.historic_data]
        target_timestamp_value = self.now.timestamp()
        regression = LinearRegression()
        regression.fit(np.array(timestamps).reshape(-1, 1), points)
        predicted = regression.predict(
            np.array([[target_timestamp_value]]))[0]
        return predicted

    def normalize_field(self, field, field_name):
        """ handle missing fields and outliers, return (value, correction) """
        field = float(field) if field != '' else None
        if field is None:
            predicted = self.predict_value(field_name)
            return (field, predicted)
        try:
            (upper_band, _, lower_band) = self.outlier_bands(field_name)
        except SensorDataNormalizationError:
            return (field, None)
        correction = None
        if field > upper_band or field < lower_band:
            predicted = self.predict_value(field_name)
            correction = predicted - field
        return (field, correction)

    def post(self, request, format=None):
        serializer = SensorUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        csv_line = request.data.get('sensors', None)

        # Cache to avoid multiple queries
        self.historic_data = SensorData.objects.all()[:self.historic_length]

        csv_data = csv.reader([csv_line])
        row = next(csv_data)
        del row[0]

        if len(row) != 12:
            return Response({'error': "Invalid number of fields"},
                            status=status.HTTP_400_BAD_REQUEST)

        self.now = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        try:
            (latitude, latitude_correction) = self.normalize_field(
                                                row[0], 'latitude')
            (longitude, longitude_correction) = self.normalize_field(
                                                 row[1], 'longitude')
            (speed_overground, speed_overground_correction) = (
                                    self.normalize_field(row[3],
                                                         'speed_overground'))
            (stw, stw_correction) = self.normalize_field(row[4], 'stw')
            (direction, direction_correction) = self.normalize_field(
                                                 row[5], 'direction')
            (current_ucomp, current_ucomp_correction) = self.normalize_field(
                                                     row[6], 'current_ucomp')
            (current_vcomp, current_vcomp_correction) = self.normalize_field(
                                                     row[7], 'current_vcomp')
            (draft_aft, draft_aft_correction) = self.normalize_field(
                                                 row[8], 'draft_aft')
            (draft_fore, draft_fore_correction) = self.normalize_field(
                                                  row[9], 'draft_fore')
            (comb_wind_swell_wave_height,
                comb_wind_swell_wave_height_correction) = (
                    self.normalize_field(row[10],
                                         'comb_wind_swell_wave_height'))
            (power, power_correction) = self.normalize_field(row[11], 'power')
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

        lookup_currents = True
        for sensor in self.historic_data:
            if sensor.sea_currents_speed is not None:
                if (self.now - sensor.datetime).total_seconds() < 600:
                    lookup_currents = False
            break
        if lookup_currents:
            try:
                currents = utils.currents_lookup(
                    sensor_data.latitude_normalized,
                    sensor_data.longitude_normalized)
            except Exception:
                currents = {'sea_currents_speed': None,
                            'sea_currents_angle': None}
        else:
            currents = {'sea_currents_speed': None,
                        'sea_currents_angle': None}
        (sea_currents_speed, sea_currents_speed_correction
         ) = self.normalize_field(
            currents['sea_currents_speed'], 'sea_currents_speed')
        (sea_currents_angle, sea_currents_angle_correction
         ) = self.normalize_field(
            currents['sea_currents_angle'], 'sea_currents_angle')
        sensor_data.sea_currents_speed = sea_currents_speed
        sensor_data.sea_currents_speed_correction = (
            sea_currents_speed_correction)
        sensor_data.sea_currents_angle = sea_currents_angle
        sensor_data.sea_currents_angle_correction = (
            sea_currents_angle_correction)
        sensor_data.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
