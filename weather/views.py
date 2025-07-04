from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import WeatherRecord, WeatherStat
from .serializers import WeatherRecordSerializer, WeatherStatSerializer
from .filters import WeatherRecordFilter

class WeatherListView(generics.ListAPIView):
    """
    API endpoint to view weather records with filtering and pagination.
    Filter by station_id and date (YYYY-MM-DD).
    """
    queryset = WeatherRecord.objects.all().order_by('station_id', 'date')
    serializer_class = WeatherRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WeatherRecordFilter

class WeatherStatsView(generics.ListAPIView):
    """
    API endpoint to view weather statistics.
    Filter by station_id and year.
    """
    queryset = WeatherStat.objects.all().order_by('station_id', 'year')
    serializer_class = WeatherStatSerializer
    filterset_fields = ['station_id', 'year']
