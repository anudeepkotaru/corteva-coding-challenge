from django.db import models


class WeatherRecord(models.Model):
    """
    Model to store raw daily weather data for a given station.

    Fields:
        - station_id: Identifier for the weather station
        - date: Date of the observation
        - max_temp: Maximum temperature of the day (in °C)
        - min_temp: Minimum temperature of the day (in °C)
        - precipitation: Precipitation for the day (in mm)
    """

    station_id = models.CharField(max_length=20)
    date = models.DateField()
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)

    class Meta:
        unique_together = (
            "station_id",
            "date",
        )  # Ensure no duplicate entries per station per day
        indexes = [
            models.Index(fields=["station_id"]),  # Index for faster station queries
            models.Index(fields=["date"]),  # Index for filtering by date
        ]


class WeatherStat(models.Model):
    """
    Model to store yearly aggregated statistics per weather station.

    Fields:
        - station_id: Identifier for the weather station
        - year: Year of aggregation
        - avg_max_temp: Average of daily max temperatures (in °C)
        - avg_min_temp: Average of daily min temperatures (in °C)
        - total_precip_cm: Total annual precipitation (in cm)
    """

    station_id = models.CharField(max_length=20)
    year = models.IntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precip_cm = models.FloatField(null=True)

    class Meta:
        unique_together = (
            "station_id",
            "year",
        )  # Ensure no duplicate entries per station per day
        indexes = [
            models.Index(fields=["station_id"]),  # Index for faster station queries
            models.Index(fields=["year"]),  # Index for filtering by year
        ]
