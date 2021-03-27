from django import forms
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientRecipe, Recipe, TagRecipe


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.ing = kwargs.pop('ingredients')
        super(RecipeForm, self).__init__(*args, **kwargs)

    tags = forms.ModelMultipleChoiceField(
        queryset=TagRecipe.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'tags__checkbox'}
        ),
        required=False
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=IngredientRecipe.objects.all(),
        required=False
    )

    class Meta:
        model = Recipe
        exclude = ('author', 'pub_date')

    def clean_ingredients(self):
        if self.ing:
            obj = []
            for name, value in self.ing.items():
                if value < 1:
                    raise ValidationError(f'Ингредиент {name} не может быть меньше 1')
                ing = get_object_or_404(Ingredient, title=name)
                ing_recipe = IngredientRecipe.objects.get_or_create(
                    ingredient=ing,
                    amount=value
                )
                obj.append(ing_recipe[0].id)
            return IngredientRecipe.objects.filter(id__in=obj)
        raise ValidationError('Необходимо добавить минимум 1 ингридиент')
