from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TagFood(models.Model):
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(verbose_name='Ингредиент', max_length=100)
    dimension = models.CharField(verbose_name='Ед.изм', max_length=10)

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredientAmounts'
    )
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return self.ingredient.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(
        verbose_name='Название рецепта',
        max_length=100,
        unique=True
    )
    tagfood = models.ManyToManyField(
        TagFood,
        verbose_name='Тэги',
        related_name='recipes',
        blank=True,
    )
    ingredient = models.ManyToManyField(
        IngredientAmount,
        verbose_name='Ингредиенты',
        related_name='recipes',
        blank=True
    )
    cook_time = models.IntegerField(verbose_name='Время приготовления')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Загрузить фото',
        upload_to='app/media/',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date', )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return self.recipe.title


class PurchaseRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return self.recipe.title


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='followers')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='followings')

    def __str__(self):
        return self.user.username
