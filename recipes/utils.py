from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientAmount, TagFood

ingres = {}
tags_food = TagFood.objects.values_list('title', flat=True)
active_tags = {k: 'active' for k in tags_food}


def filter_tags(request) -> list:
    for tag in TagFood.objects.values_list('title', flat=True):
        item = request.GET.get(tag)
        if item != active_tags[tag] and item is not None:
            active_tags[tag] = item
    tags = [k for k, v in active_tags.items() if v == 'active']
    return tags


def get_ingredients(request, query_name, query_value):
    for key, value in request.POST.items():
        if key.startswith(query_name):
            num = key.split('_')[1]
            ingres[value] = request.POST.get(f'{query_value}_{num}')
    return ingres


def save_recipe(request, form, ingredient: dict):
    try:
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        with transaction.atomic():
            data = form.cleaned_data.get('tagfood')
            for tag in data:
                tag.recipes.add(recipe)

            recipe.ingredient.all().delete()
            for title, value in ingredient.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                ingredient_amount = IngredientAmount.objects.get_or_create(
                    ingredient=ingredient,
                    amount=value)
                ingredient_amount[0].recipes.add(recipe)
            recipe.save()

            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest
