from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, MeasurementViewSet

# Создаём роутер и регистрируем ViewSets
router = DefaultRouter()
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'measurements', MeasurementViewSet, basename='measurement')

urlpatterns = [
    path('', include(router.urls)),
]