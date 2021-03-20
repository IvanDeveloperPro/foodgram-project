from django import forms
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientRecipe, Recipe, TagRecipe


class RecipeForm(forms.ModelForm):

    tag_recipes = forms.ModelMultipleChoiceField(
        queryset=TagRecipe.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'tags__checkbox'}
        ),
        required=False
    )
    ingredient_recipes = forms.ModelMultipleChoiceField(
        queryset=IngredientRecipe.objects.all(),
        required=False
    )

    class Meta:
        model = Recipe
        exclude = ('author', 'pub_date')


def save_recipe(request, form, ingredient: dict):
    try:
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        data = form.cleaned_data.get('tag_recipes')
        for tag in data:
            tag.recipes.add(recipe)

        with transaction.atomic():
            recipe.ingredient_recipes.all().delete()

            for title, value in ingredient.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                ingredient_amount = IngredientRecipe.objects.get_or_create(
                    ingredient=ingredient,
                    amount=value)
                ingredient_amount[0].recipes.add(recipe)
            recipe.save()

        return recipe
    except IntegrityError:
        raise HttpResponseBadRequest
