import django_filters
from datetime import datetime
from .models import WeatherRecord

class WeatherRecordFilter(django_filters.FilterSet):
    date = django_filters.CharFilter(method='filter_date')

    def filter_date(self, queryset, name, value):
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
        fields = ['station_id', 'date']