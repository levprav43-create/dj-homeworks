from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}
from django.shortcuts import render


def recipe_view(request, recipe_name):
    """
    Показывает ингредиенты рецепта.
    Поддерживает параметр ?servings=N для умножения порций.
    """
    # Получаем количество порций (по умолчанию 1)
    servings = request.GET.get('servings', 1)
    
    # Пробуем преобразовать в число
    try:
        servings = int(servings)
        if servings < 1:
            servings = 1
    except (ValueError, TypeError):
        servings = 1
    
    # Получаем рецепт из DATA
    recipe = DATA.get(recipe_name)
    
    # Если рецепт не найден — возвращаем пустой контекст
    if not recipe:
        return render(request, 'calculator/index.html', {'recipe': None})
    
    # Умножаем ингредиенты на количество порций
    recipe_context = {}
    for ingredient, amount in recipe.items():
        recipe_context[ingredient] = amount * servings
    
    # Формируем контекст
    context = {
        'recipe': recipe_context
    }
    
    # Рендерим шаблон
    return render(request, 'calculator/index.html', context)
# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
