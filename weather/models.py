from django.db import models


class WeatherRecord(models.Model):
    station_id = models.CharField(max_length=20)
    date = models.DateField()
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)

    class Meta:
        unique_together = ("station_id", "date")
        indexes = [
            models.Index(fields=["station_id"]),
            models.Index(fields=["date"]),
        ]


class WeatherStat(models.Model):
    station_id = models.CharField(max_length=20)
    year = models.IntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precip_cm = models.FloatField(null=True)

    class Meta:
        unique_together = ("station_id", "year")
        indexes = [
            models.Index(fields=["station_id"]),
            models.Index(fields=["year"]),
        ]
