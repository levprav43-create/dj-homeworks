from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    """Продукт"""
    title = models.CharField(max_length=60, unique=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Stock(models.Model):
    """Склад"""
    address = models.CharField(max_length=200, unique=True, verbose_name='Адрес')
    products = models.ManyToManyField(
        Product,
        through='StockProduct',
        related_name='stocks',
        verbose_name='Продукты'
    )
    
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
        ordering = ['address']
    
    def __str__(self):
        return self.address


class StockProduct(models.Model):
    """Остаток продукта на складе"""
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Склад'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость хранения'
    )
    
    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'
        ordering = ['stock', 'product']
        constraints = [
            models.UniqueConstraint(fields=['stock', 'product'], name='unique_stock_product')
        ]
    
    def __str__(self):
        return f'{self.product.title} на {self.stock.address}: {self.quantity} шт.'