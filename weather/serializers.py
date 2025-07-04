from rest_framework import serializers
from .models import WeatherRecord, WeatherStat

class WeatherRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields = '__all__'

class WeatherStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStat
        fields = '__all__'
