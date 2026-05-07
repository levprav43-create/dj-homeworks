from django.db import models
from django.contrib.auth.models import User


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления"""
    OPEN = 'OPEN', 'Открыто'
    CLOSED = 'CLOSED', 'Закрыто'


class Advertisement(models.Model):
    """Объявление"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(
        max_length=10,
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
        verbose_name='Статус'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='advertisements',
        verbose_name='Создатель'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'