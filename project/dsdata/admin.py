from django.contrib import admin
from .models import SensorData


class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'latitude',
        'longitude',
        'datetime',
        'speed_overground',
        'stw',
        'direction',
        'current_ucomp',
        'current_vcomp',
        'draft_aft',
        'draft_fore',
        'comb_wind_swell_wave_height',
        'power',
    )


admin.site.register(SensorData, SensorDataAdmin)
