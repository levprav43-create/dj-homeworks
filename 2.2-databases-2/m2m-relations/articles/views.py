from django.shortcuts import render
from articles.models import Article


def articles_list(request):
    """Отображает список статей с тегами"""
    template = 'articles/news.html'
    
    # Получаем параметр сортировки из GET-запроса (по умолчанию - новые сначала)
    ordering = request.GET.get('order_by', '-published_at')
    
    # Получаем статьи с предзагрузкой тегов (оптимизация запросов)
    articles = Article.objects.prefetch_related('scopes__tag').order_by(ordering)
    
    context = {
        'object_list': articles,
        'current_order': ordering
    }
    
    return render(request, template, context)