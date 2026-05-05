from rest_framework import serializers
from .models import Product, Stock, StockProduct


class StockProductSerializer(serializers.ModelSerializer):
    """Сериализатор для остатков на складе"""
    
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = StockProduct
        fields = ['id', 'stock', 'product', 'quantity', 'price']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов с вложенными остатками"""
    
    positions = StockProductSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'positions']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Создание продукта + остатков"""
        positions_data = validated_data.pop('positions', [])
        product = Product.objects.create(**validated_data)
        
        for pos_data in positions_data:
            StockProduct.objects.create(
                product=product,
                stock=pos_data['stock'],  # 🔧 Теперь передаём объект
                quantity=pos_data.get('quantity', 1),
                price=pos_data.get('price', 0)
            )
        return product
    
    def update(self, instance, validated_data):
        """Обновление продукта + остатков"""
        positions_data = validated_data.pop('positions', [])
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # Удаляем старые остатки и создаём новые
        instance.positions.all().delete()
        for pos_data in positions_data:
            StockProduct.objects.create(
                product=instance,
                stock=pos_data['stock'],  # 🔧 Теперь передаём объект
                quantity=pos_data.get('quantity', 1),
                price=pos_data.get('price', 0)
            )
        return instance


class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для складов с вложенными остатками"""
    
    positions = StockProductSerializer(read_only=True, many=True, source='positions.select_related("product")')
    
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']
        read_only_fields = ['id']