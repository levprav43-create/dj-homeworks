from django.db import models


class Teacher(models.Model):
    """Учитель"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    subject = models.CharField(max_length=100, verbose_name='Предмет')
    
    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} ({self.subject})'


class Student(models.Model):
    """Ученик"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    # 🔧 МЕНЯЕМ: ForeignKey → ManyToManyField
    teachers = models.ManyToManyField(Teacher, related_name='students', verbose_name='Учителя')
    
    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['name']
    
    def __str__(self):
        return self.name