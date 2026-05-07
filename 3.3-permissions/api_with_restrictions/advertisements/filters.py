import django_filters
from .models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(django_filters.FilterSet):
    """Фильтры для объявлений"""
    
    # Фильтрация по дате создания (диапазон)
    created_at = django_filters.DateFromToRangeFilter()
    
    # Фильтрация по статусу
    status = django_filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    
    class Meta:
        model = Advertisement
        fields = ['status', 'created_at']