from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormSet(BaseInlineFormSet):
    """Формсет для проверки что есть один и только один основной тег"""
    
    def clean(self):
        super().clean()
        
        # Считаем сколько основных тегов
        main_count = 0
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data.get('is_main'):
                main_count += 1
        
        # Проверяем что есть ровно один основной тег
        if main_count == 0:
            raise ValidationError('Укажите хотя бы один основной тег!')
        if main_count > 1:
            raise ValidationError('Основной тег должен быть только один!')
        
        return self.cleaned_data


class ScopeInline(admin.TabularInline):
    """Inline для связи статья-тег"""
    model = Scope
    extra = 1
    formset = ScopeInlineFormSet


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админка для статей"""
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']
    list_filter = ['tags']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для тегов"""
    list_display = ['name']