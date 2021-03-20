from django import template
from django.shortcuts import get_object_or_404

from recipes.models import FavoriteRecipe, Follow, PurchaseRecipe, TagRecipe

from ..utils import active_tags

register = template.Library()


@register.filter
def tag_filter(tag):
    label = tag.data.get('label')
    food_tag = get_object_or_404(TagRecipe, title=label)
    style = f'tags__checkbox tags__checkbox_style_{food_tag.color}'
    tag.data['attrs']['class'] = style
    return tag


@register.filter
def active_tag(tag):
    return active_tags[tag.title]


@register.filter
def user_purchase(recipe, request):
    if request.user.is_anonymous:
        return False
    else:
        return PurchaseRecipe.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()


@register.filter
def user_favorite(recipe, request):
    if request.user.is_authenticated:
        return FavoriteRecipe.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()


@register.filter
def follow(recipe, request):
    if request.user.is_authenticated:
        return Follow.objects.filter(
            user=request.user,
            author=recipe.author
        ).exists()


@register.filter
def author_follow(author, request):
    if request.user.is_authenticated:
        return Follow.objects.filter(
            user=request.user,
            author=author
        ).exists()


@register.filter
def count_recipes(num):
    excl_nums = [11, 12, 13, 14]
    if num == 0:
        return 'Нет больше рецептов'
    elif num % 10 == 1 and num not in excl_nums:
        return f'Еще {num} рецепт'
    elif 2 <= num % 10 <= 4 and num not in excl_nums:
        return f'Еще {num} рецепта'
    else:
        return f'Еще {num} рецептов'
