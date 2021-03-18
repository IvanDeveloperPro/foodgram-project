from django import forms

from .models import IngredientAmount, Recipe, TagFood


class RecipeForm(forms.ModelForm):

    tagfood = forms.ModelMultipleChoiceField(
        queryset=TagFood.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'tags__checkbox'}
        ),
        required=False
    )
    ingredient = forms.ModelMultipleChoiceField(
        queryset=IngredientAmount.objects.all(),
        required=False
    )

    class Meta:
        model = Recipe
        exclude = ('author', 'pub_date')
