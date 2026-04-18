from django.shortcuts import render
from school.models import Student


def students_list(request):
    """Отображает список учеников с учителями"""
    template = 'school/students_list.html'
    
    # Получаем параметр сортировки из GET-запроса (по умолчанию - по имени)
    ordering = request.GET.get('order_by', 'name')
    
    # Получаем учеников с предзагрузкой учителей (оптимизация запросов)
    students = Student.objects.prefetch_related('teachers').order_by(ordering)
    
    context = {
        'object_list': students,
        'current_order': ordering
    }
    
    return render(request, template, context)