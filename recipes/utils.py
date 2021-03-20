from .models import Recipe, TagRecipe

tag_recipes = TagRecipe.objects.values_list('title', flat=True)
active_tags = {k: 'active' for k in tag_recipes}
# в active_tags я храню состяние всех тегов.
# При фильтрации по тегам здесь сохраняю их текущее состояние.
# прошу подсказать , где можно хранить состояние


def filter_tags(request) -> list:
    for tag in active_tags:
        item = request.GET.get(tag)
        if item != active_tags.get(tag) and item is not None:
            active_tags[tag] = item
    tags = [k for k, v in active_tags.items() if v == 'active']
    return tags


def get_ingredients(request, query_name, query_value):
    ingres = {}
    for key, value in request.POST.items():
        if key.startswith(query_name):
            num = key.split('_')[1]
            ingres[value] = request.POST.get(f'{query_value}_{num}')
    return ingres


def filter_recipes(request):
    return (
        Recipe.objects
        .select_related('author')
        .prefetch_related('ingredient_recipes', 'tag_recipes')
        .filter(tag_recipes__title__in=filter_tags(request))
        .distinct()
    )
