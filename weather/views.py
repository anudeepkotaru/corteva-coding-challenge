from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import WeatherRecord, WeatherStat
from .serializers import WeatherRecordSerializer, WeatherStatSerializer
from .filters import WeatherRecordFilter

class WeatherListView(generics.ListAPIView):
    queryset = WeatherRecord.objects.all().order_by('date')
    serializer_class = WeatherRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WeatherRecordFilter

class WeatherStatsView(generics.ListAPIView):
    queryset = WeatherStat.objects.all().order_by('year')
    serializer_class = WeatherStatSerializer
    filterset_fields = ['station_id', 'year']
