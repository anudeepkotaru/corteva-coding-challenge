import django_filters
from datetime import datetime
from .models import WeatherRecord

class WeatherRecordFilter(django_filters.FilterSet):
    date = django_filters.CharFilter(method='filter_date')

    def filter_date(self, queryset, name, value):
        try:
            # Convert YYYYMMDD to YYYY-MM-DD
            parsed_date = datetime.strptime(value, "%Y%m%d").date()
            return queryset.filter(date=parsed_date)
        except ValueError:
            return queryset.none()

    class Meta:
        model = WeatherRecord
        fields = ['station_id', 'date']
