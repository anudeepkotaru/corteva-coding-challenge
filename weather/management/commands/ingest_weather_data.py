import os
import pathlib
from tqdm import tqdm
import logging
from datetime import datetime
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from weather.models import WeatherRecord


# Logging for tracking progress and errors
LOG_FILE = "weather_ingestion.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# --------- PARSE FUNCTION ---------
def parse_line(line: str, station_id: str) -> WeatherRecord | None:
    """Convert one line of the raw file into a :class:`WeatherRecord` instance.

    Parameters
    ----------
    line : str
        The raw input is a tab‑delimited line with (``YYYYMMDD    max_temp    min_temp    prcp``).
    station_id : str
        station_id is extracted from the file name.

    Returns
    -------
    WeatherRecord | None
        Parsed model instance or None if the line is empty.
    """
    if not line.strip():
        return None  # skips empty line

    try:
        date_str, t_max, t_min, prcp = line.split("\t")
        date = datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError as e:
        logging.warning(f"Failed to parse line: {line.strip()} | Error: {e}")
        return None

    # Convert missing values (‑9999) to None
    def check_for_none(value: str) -> float | None:
        num = int(value)
        if num == -9999:
            return None
        else:
            num = int(num) / 10
            return num

    return WeatherRecord(
        station_id=station_id,
        date=date,
        max_temp=check_for_none(t_max),
        min_temp=check_for_none(t_min),
        precipitation=check_for_none(prcp),
    )


class Command(BaseCommand):
    """Load raw weather data files into the database."""

    help = "Ingest weather data from text files into the WeatherRecord model."

    def handle(self, *args, **kwargs):
        try:
            WX_DATA_DIR = "wx_data"
            data_dir = pathlib.Path(WX_DATA_DIR).resolve()
            batch_size = 5000

            if not data_dir.exists():
                raise CommandError(f"Directory not found: {data_dir}")
            start_time = datetime.now()
            logging.info(f"Starting ingestion from {data_dir} at {start_time}")

            total_records = 0
            created_records = 0

            for filename in tqdm(os.listdir(data_dir)):
                if not filename.endswith(".txt"):
                    continue
                station_id = filename.replace(
                    ".txt", ""
                )  # Extracting station_id from filename
                file_path = os.path.join(data_dir, filename)

                with open(file_path, "r", encoding="utf-8") as f:
                    buffer: List[WeatherRecord] = []

                    for line in f:
                        total_records += 1
                        record = parse_line(line, station_id)
                        if record:
                            buffer.append(record)

                        if len(buffer) >= batch_size:
                            created_records += self._bulk_insert(buffer)
                            buffer.clear()

                    if buffer:
                        created_records += self._bulk_insert(buffer)

            end_time = datetime.now()
            logging.info(
                f"Ingested {created_records} records in {(end_time - start_time).total_seconds()} seconds."
            )
        except Exception as e:
            logging.critical(f"Ingestion failed: {e}")

    @staticmethod
    @transaction.atomic
    def _bulk_insert(records: List[WeatherRecord]) -> int:
        if not records:
            return 0
        result = WeatherRecord.objects.bulk_create(records, ignore_conflicts=True)
        return len(result)
