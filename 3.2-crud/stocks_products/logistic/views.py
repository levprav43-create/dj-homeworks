from rest_framework import viewsets, filters
from django.db.models import Prefetch
from .models import Product, Stock, StockProduct
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с продуктами"""
    queryset = Product.objects.prefetch_related(
        Prefetch('positions', queryset=StockProduct.objects.select_related('stock'))
    )
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(viewsets.ModelViewSet):
    """ViewSet для работы со складами"""
    queryset = Stock.objects.prefetch_related(
        Prefetch('positions', queryset=StockProduct.objects.select_related('product'))
    )
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    
    def get_queryset(self):
        """Фильтрация складов по product_id из запроса"""
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        
        if product_id:
            queryset = queryset.filter(positions__product_id=product_id).distinct()
        
        return queryset