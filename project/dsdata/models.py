from django.db import models


class SensorData(models.Model):
    class Meta:
        ordering = ['-datetime']

    datetime = models.DateTimeField()

    latitude = models.FloatField(null=True, blank=True)
    latitude_correction = models.FloatField(null=True, blank=True)

    @property
    def latitude_normalized(self):
        return (self.latitude or 0.0) + (self.latitude_correction or 0.0)

    longitude = models.FloatField(null=True, blank=True)
    longitude_correction = models.FloatField(null=True, blank=True)

    @property
    def longitude_normalized(self):
        return (self.longitude or 0.0) + (self.longitude_correction or 0.0)

    speed_overground = models.FloatField(null=True, blank=True)
    speed_overground_correction = models.FloatField(null=True, blank=True)

    @property
    def speed_overground_normalized(self):
        return ((self.speed_overground or 0.0) +
                (self.speed_overground_correction or 0.0))

    stw = models.FloatField(null=True, blank=True)
    stw_correction = models.FloatField(null=True, blank=True)

    @property
    def stw_normalized(self):
        return ((self.stw or 0.0) + (self.stw_correction or 0.0))

    direction = models.FloatField(null=True, blank=True)
    direction_correction = models.FloatField(null=True, blank=True)

    @property
    def direction_normalized(self):
        return ((self.direction or 0.0) +
                (self.direction_correction or 0.0))

    current_ucomp = models.FloatField(null=True, blank=True)
    current_ucomp_correction = models.FloatField(null=True, blank=True)

    @property
    def current_ucomp_normalized(self):
        return ((self.current_ucomp or 0.0) +
                (self.current_ucomp_correction or 0.0))

    current_vcomp = models.FloatField(null=True, blank=True)
    current_vcomp_correction = models.FloatField(null=True, blank=True)

    @property
    def current_vcomp_normalized(self):
        return ((self.current_vcomp or 0.0) +
                (self.current_vcomp_correction or 0.0))

    draft_aft = models.FloatField(null=True, blank=True)
    draft_aft_correction = models.FloatField(null=True, blank=True)

    @property
    def draft_aft_normalized(self):
        return ((self.draft_aft or 0.0) +
                (self.draft_aft_correction or 0.0))

    draft_fore = models.FloatField(null=True, blank=True)
    draft_fore_correction = models.FloatField(null=True, blank=True)

    @property
    def draft_fore_normalized(self):
        return ((self.draft_fore or 0.0) +
                (self.draft_fore_correction or 0.0))

    comb_wind_swell_wave_height = models.FloatField(null=True, blank=True)
    comb_wind_swell_wave_height_correction = models.FloatField(
        null=True, blank=True)

    @property
    def comb_wind_swell_wave_height_normalized(self):
        return ((self.comb_wind_swell_wave_height or 0.0) +
                (self.comb_wind_swell_wave_height_correction or 0.0))

    power = models.FloatField(null=True, blank=True)
    power_correction = models.FloatField(null=True, blank=True)

    @property
    def power_normalized(self):
        return ((self.power or 0.0) + (self.power_correction or 0.0))

    def __str__(self):
        return (f"SensorData({self.latitude}, "
                f"{self.longitude}, {self.datetime})")
