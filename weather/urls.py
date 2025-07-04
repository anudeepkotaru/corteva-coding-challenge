from django.urls import path
from .views import WeatherListView, WeatherStatsView

urlpatterns = [
    path('weather', WeatherListView.as_view()),
    path('weather/stats', WeatherStatsView.as_view()),
]
