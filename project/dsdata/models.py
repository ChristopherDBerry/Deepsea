from django.db import models


class SensorData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    datetime = models.DateTimeField()
    speed_overground = models.FloatField()
    stw = models.FloatField()
    direction = models.FloatField()
    current_ucomp = models.FloatField()
    current_vcomp = models.FloatField()
    draft_aft = models.FloatField()
    draft_fore = models.FloatField()
    comb_wind_swell_wave_height = models.FloatField()
    power = models.FloatField()

    def __str__(self):
        return f"SensorData({self.latitude}, {self.longitude}, {self.datetime})"
