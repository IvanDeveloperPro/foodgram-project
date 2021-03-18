from django.contrib import admin

from .models import (FavoriteRecipe, Follow, Ingredient, IngredientAmount,
                     PurchaseRecipe, Recipe, TagFood)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'cook_time',
        'description',
        'image',
    )
    search_fields = ('title',)
    list_filter = ('pub_date', 'title')


class TagFoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagFood, TagFoodAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(FavoriteRecipe)
admin.site.register(PurchaseRecipe)
admin.site.register(Follow)
