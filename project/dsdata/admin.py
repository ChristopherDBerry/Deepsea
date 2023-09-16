from django.contrib import admin
from .models import SensorData


class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'datetime',
        'latitude',
        'latitude_correction',
        'latitude_normalized',
        'longitude',
        'longitude_correction',
        'longitude_normalized',
        'speed_overground',
        'speed_overground_correction',
        'speed_overground_normalized',
        'stw',
        'stw_correction',
        'stw_normalized',
        'direction',
        'direction_correction',
        'direction_normalized',
        'current_ucomp',
        'current_ucomp_correction',
        'current_ucomp_normalized',
        'current_vcomp',
        'current_vcomp_correction',
        'current_vcomp_normalized',
        'draft_aft',
        'draft_aft_correction',
        'draft_aft_normalized',
        'draft_fore',
        'draft_fore_correction',
        'draft_fore_normalized',
        'comb_wind_swell_wave_height',
        'comb_wind_swell_wave_height_correction',
        'comb_wind_swell_wave_height_normalized',
        'power',
        'power_correction',
        'power_normalized',
        'sea_currents_speed',
        'sea_currents_speed_correction',
        'sea_currents_speed_normalized',
        'sea_currents_angle',
        'sea_currents_angle_correction',
        'sea_currents_angle_normalized',
    )


admin.site.register(SensorData, SensorDataAdmin)
