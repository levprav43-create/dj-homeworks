from django.db import models


class Sensor(models.Model):
    """Датчик температуры"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Измерение температуры"""
    sensor = models.ForeignKey(
        Sensor, 
        on_delete=models.CASCADE, 
        related_name='measurements',
        verbose_name='Датчик'
    )
    temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        verbose_name='Температура'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Время измерения'
    )
    
    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.sensor.name}: {self.temperature}°C'