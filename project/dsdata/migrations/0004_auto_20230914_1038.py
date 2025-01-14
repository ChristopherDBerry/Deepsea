# Generated by Django 3.2.5 on 2023-09-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsdata', '0003_auto_20230914_0905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensordata',
            options={'ordering': ['-datetime']},
        ),
        migrations.AddField(
            model_name='sensordata',
            name='comb_wind_swell_wave_height_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='current_ucomp_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='current_vcomp_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='direction_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='draft_aft_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='draft_fore_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='longitude_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='power_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='speed_overground_correction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='stw_correction',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
