import os
import shutil
from pathlib import Path
from django.core.management import call_command
from django.test import TestCase
from weather.models import WeatherRecord, WeatherStat

class WeatherIngestionAndStatsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a temporary test data directory and a sample .txt file
        cls.test_data_dir = Path("wx_data")
        cls.test_data_dir.mkdir(exist_ok=True)

        sample_file = cls.test_data_dir / "TEST0001.txt"
        sample_file.write_text(
            """
            19850101	23	-55	12
            19850102	25	-50	15
            19850103	-9999	-9999	-9999
            19850104	30	-45	20
            """.strip(),
            encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Clean up the test directory after tests
        if cls.test_data_dir.exists():
            shutil.rmtree(cls.test_data_dir)

    def test_ingest_weather_data(self):
        # Run the ingestion command
        call_command("ingest_weather")

        # Check that only 3 valid records were ingested
        records = WeatherRecord.objects.filter(station_id="TEST0001")
        self.assertEqual(records.count(), 3)

        # Check one of the parsed values
        jan_2 = records.get(date="1985-01-02")
        self.assertEqual(jan_2.max_temp, 2.5)
        self.assertEqual(jan_2.min_temp, -5.0)
        self.assertEqual(jan_2.precipitation, 1.5)

    def test_compute_weather_stats(self):
        # Run ingestion first to create WeatherRecords
        call_command("ingest_weather")

        # Then run the stats computation
        call_command("compute_weather_stats")

        # Should have one WeatherStat record
        stats = WeatherStat.objects.filter(station_id="TEST0001", year=1985)
        self.assertEqual(stats.count(), 1)

        stat = stats.first()

        # Calculated values:
        # avg_max = (2.3 + 2.5 + 3.0) / 3 = 2.6
        # avg_min = (-5.5 + -5.0 + -4.5) / 3 = -5.0
        # total_prcp = (1.2 + 1.5 + 2.0) = 4.7 cm
        self.assertEqual(stat.avg_max_temp, 2.6, places=2)
        self.assertEqual(stat.avg_min_temp, -5.0, places=2)
        self.assertEqual(stat.total_precip_cm, 4.7, places=2)
