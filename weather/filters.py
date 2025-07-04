import django_filters
from datetime import datetime
from .models import WeatherRecord


class WeatherRecordFilter(django_filters.FilterSet):
    """
    Custom filter set for WeatherRecord.

    Allows filtering weather records by:
        - station_id: exact match
        - date: supports both 'YYYYMMDD' and 'YYYY-MM-DD' formats

    The 'date' field uses a custom method to handle multiple input formats.
    """

    date = django_filters.CharFilter(method="filter_date")

    def filter_date(self, queryset, name, value):
        """
        Custom filter method for parsing date strings.

        Attempts to parse the input date using two common formats:
            - YYYYMMDD (e.g., 19850101)
            - YYYY-MM-DD (e.g., 1985-01-01)

        Returns:
            - Filtered queryset if date is parsed successfully
            - Empty queryset if parsing fails
        """

        parsed_date = None
        for fmt in ("%Y%m%d", "%Y-%m-%d"):
            try:
                parsed_date = datetime.strptime(value, fmt).date()
                break
            except ValueError:
                continue

        if parsed_date:
            return queryset.filter(date=parsed_date)
        return queryset.none()

    class Meta:
        model = WeatherRecord
        fields = ["station_id", "date"]     # Supported filter fields
