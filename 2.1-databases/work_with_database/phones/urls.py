from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/<slug:slug>/', views.phone_detail, name='phone'),
]