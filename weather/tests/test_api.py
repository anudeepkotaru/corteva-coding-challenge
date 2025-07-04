from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from weather.models import WeatherRecord, WeatherStat


class WeatherAPITestCase(TestCase):
    def setUp(self):
        # Create an APIClient instance for making HTTP requests
        self.client = APIClient()

        # Create two weather records
        WeatherRecord.objects.create(
            station_id="USC001",
            date=date(1985, 1, 1),
            max_temp=100,
            min_temp=50,
            precipitation=200,
        )
        WeatherRecord.objects.create(
            station_id="USC002",
            date=date(1985, 1, 2),
            max_temp=110,
            min_temp=60,
            precipitation=250,
        )

        # Create one weather stat entry
        WeatherStat.objects.create(
            station_id="USC001",
            year=1985,
            avg_max_temp=10.0,
            avg_min_temp=5.0,
            total_precip_cm=20.0,
        )

    def test_get_weather_records(self):
        """
        Test fetching all weather records.
        Should return 2 records created in setUp.
        """
        response = self.client.get("/api/weather")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_weather_records_by_date_format_yyyymmdd(self):
        """
        Test filtering weather records using date in YYYYMMDD format.
        """
        response = self.client.get("/api/weather?date=19850101")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["station_id"], "USC001")

    def test_get_weather_records_by_date_format_yyyy_mm_dd(self):
        """
        Test filtering weather records using date in YYYY-MM-DD format.
        """
        response = self.client.get("/api/weather?date=1985-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_weather_records_by_station(self):
        """
        Test filtering weather records by station_id.
        """
        response = self.client.get("/api/weather?station_id=USC002")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_weather_stats(self):
        """
        Test fetching all weather statistics.
        Should return the one stat created in setUp.
        """
        response = self.client.get("/api/weather/stats")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["year"], 1985)

    def test_get_weather_stats_by_station(self):
        """
        Test filtering weather stats by station_id.
        """
        response = self.client.get("/api/weather/stats?station_id=USC001")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_weather_stats_by_year(self):
        """
        Test filtering weather stats by year.
        """
        response = self.client.get("/api/weather/stats?year=1985")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
