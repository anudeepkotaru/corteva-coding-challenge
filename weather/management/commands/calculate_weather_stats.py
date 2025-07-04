from datetime import datetime
from collections import defaultdict
import logging

from django.core.management.base import BaseCommand
from weather.models import WeatherRecord, WeatherStat

# from django.db.models import Avg, Sum
# from django.db.models.functions import ExtractYear
from django.db import transaction


# Logging for tracking progress and errors
LOG_FILE = "compute_stats.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class Command(BaseCommand):
    """
    Django management command to compute yearly statistics for each weather station.

    Statistics include:
        - Average maximum temperature (in degrees Celsius)
        - Average minimum temperature (in degrees Celsius)
        - Total accumulated precipitation (in centimeters)

    This command will:
        - Group weather records by station and year
        - Ignore missing data (None)
        - Calculate and store the stats in the WeatherStat model
        - Overwrite existing stats on each run
    """

    help = "Calculate yearly weather statistics per station"

    def handle(self, *args, **kwargs):
        try:
            start_time = datetime.now()
            logging.info("[START] Yearly stats computation started at %s", start_time)

            # Clear old stats to avoid duplicates
            WeatherStat.objects.all().delete()
            logging.info("Cleared existing WeatherStat records.")

            # Retrieve all weather records
            records = WeatherRecord.objects.all()
            logging.info(f"Fetched {records.count()} weather records.")

            # Dictionary to group records by (station_id, year)
            stats_map = defaultdict(list)
            for record in records:
                year = record.date.year
                stats_map[(record.station_id, year)].append(record)

            to_create = []

            for (station_id, year), recs in stats_map.items():
                # Extract non-null temperature and precipitation values
                max_vals = [r.max_temp for r in recs if r.max_temp is not None]
                min_vals = [r.min_temp for r in recs if r.min_temp is not None]
                prcp_vals = [
                    r.precipitation for r in recs if r.precipitation is not None
                ]

                # Compute average and totals
                avg_max = round(sum(max_vals) / len(max_vals), 2) if max_vals else None
                avg_min = round(sum(min_vals) / len(min_vals), 2) if min_vals else None
                total_prcp = (
                    round(sum(prcp_vals) / 10, 2) if prcp_vals else None
                )  # convert mm to cm

                # Create WeatherStat object
                to_create.append(
                    WeatherStat(
                        station_id=station_id,
                        year=year,
                        avg_max_temp=avg_max,
                        avg_min_temp=avg_min,
                        total_precip_cm=total_prcp,
                    )
                )

            # Bulk insert all computed stats
            with transaction.atomic():
                WeatherStat.objects.bulk_create(to_create, batch_size=500)
            logging.info(f"Inserted {len(to_create)} records into yearly stats table.")

            end_time = datetime.now()
            logging.info(f"Completed computing yearly stats in {end_time - start_time}")
        except Exception as e:
            logging.critical(f"Computation failed: {e}")
