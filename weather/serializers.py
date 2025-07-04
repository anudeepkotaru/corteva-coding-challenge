from rest_framework import serializers
from .models import WeatherRecord, WeatherStat


class WeatherRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the WeatherRecord model.
    """

    class Meta:
        model = WeatherRecord
        fields = "__all__"


class WeatherStatSerializer(serializers.ModelSerializer):
    """
    Serializer for the WeatherRecord model.
    """
    class Meta:
        model = WeatherStat
        fields = "__all__"
