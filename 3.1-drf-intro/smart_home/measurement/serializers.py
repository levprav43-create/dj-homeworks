from rest_framework import serializers
from .models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для вложенных измерений (только чтение)"""
    
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']
        read_only_fields = ['created_at']


class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого списка датчиков"""
    
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о датчике с измерениями"""
    
    measurements = MeasurementSerializer(read_only=True, many=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']


class MeasurementCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового измерения"""
    
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at']
        read_only_fields = ['created_at']