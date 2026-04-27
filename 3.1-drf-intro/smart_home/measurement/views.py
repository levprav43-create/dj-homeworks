from rest_framework import viewsets
from .models import Sensor, Measurement
from .serializers import (
    SensorSerializer,
    SensorDetailSerializer,
    MeasurementCreateSerializer
)


class SensorViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с датчиками: CRUD"""
    queryset = Sensor.objects.all()
    
    def get_serializer_class(self):
        """Возвращаем нужный сериализатор в зависимости от действия"""
        if self.action == 'retrieve':
            return SensorDetailSerializer
        return SensorSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с измерениями: Create, Read"""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer