from django.shortcuts import render, get_object_or_404
from phones.models import Phone


def catalog_view(request):
    """Отображает каталог телефонов с сортировкой"""
    # Получаем параметр сортировки из GET-запроса
    sort_param = request.GET.get('sort', 'name')
    
    # Определяем порядок сортировки
    if sort_param == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sort_param == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:  # name или по умолчанию
        phones = Phone.objects.all().order_by('name')
    
    context = {
        'phones': phones,
        'current_sort': sort_param
    }
    return render(request, 'catalog.html', context)


def phone_detail(request, slug):
    """Отображает详细信息 о телефоне"""
    phone = get_object_or_404(Phone, slug=slug)
    context = {
        'phone': phone
    }
    return render(request, 'product.html', context)