from django.contrib import admin

from .models import (FavoriteRecipe, Follow, Ingredient, IngredientRecipe,
                     PurchaseRecipe, Recipe, TagRecipe)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'cook_time',
        'description',
        'image',
    )
    search_fields = ('title',)
    list_filter = ('pub_date', 'title')


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(FavoriteRecipe)
admin.site.register(PurchaseRecipe)
admin.site.register(Follow)
