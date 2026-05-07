"""api_with_restrictions URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('advertisements.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Для login/logout в браузере
]