from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.URLField(verbose_name='Изображение')
    release_date = models.DateField(verbose_name='Дата выхода')
    lte_exists = models.BooleanField(default=False, verbose_name='LTE')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    def save(self, *args, **kwargs):
        # Автоматически создаём slug из name если его нет
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        ordering = ['name']