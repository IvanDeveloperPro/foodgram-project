from django.core.cache import cache

from .models import Recipe, TagRecipe


def get_tags():
    return TagRecipe.objects.values_list('title', flat=True)


def filter_tags(request) -> list:
    tags = []
    for tag in get_tags():
        if tag not in cache:
            cache.set(tag, 'active')
        item = request.GET.get(tag)
        if item != cache.get(tag) and item is not None:
            cache.set(tag, item)
        if cache.get(tag) == 'active':
            tags.append(tag)
    return tags


def get_ingredients_dict(request, query_name, query_value):
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith(query_name):
            num = key.split('_')[1]
            ingredients[value] = request.POST.get(f'{query_value}_{num}')
    return ingredients


def filter_recipes(request):
    return (
        Recipe.objects
        .select_related('author')
        .prefetch_related('ingredients', 'tags')
        .filter(tags__title__in=filter_tags(request))
        .distinct()
    )
