from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TagRecipe(models.Model):
    title = models.CharField(
        verbose_name='Вид приема пищи',
        max_length=20
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=20
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name='Ингредиент',
        max_length=100
    )
    dimension = models.CharField(
        verbose_name='Ед.изм',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipes'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return self.ingredient.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(
        verbose_name='Название рецепта',
        max_length=100,
        unique=True
    )
    tag_recipes = models.ManyToManyField(
        TagRecipe,
        verbose_name='Тэги',
        related_name='recipes',
        blank=True,
    )
    ingredient_recipes = models.ManyToManyField(
        IngredientRecipe,
        verbose_name='Ингредиенты',
        related_name='recipes',
        blank=True
    )
    cook_time = models.PositiveIntegerField(verbose_name='Время приготовления')
    description = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(
        verbose_name='Загрузить фото',
        upload_to='app/media/',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return self.recipe.title


class PurchaseRecipe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Владелец списка покупок',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт списка покупок',
        on_delete=models.CASCADE,
        related_name='purchases',
    )

    class Meta:
        verbose_name = 'Рецепт списка покупок'
        verbose_name_plural = 'Рецепты списка покупок'

    def __str__(self):
        return self.recipe.title


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='followers',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Авторы',
        on_delete=models.CASCADE,
        related_name='followings'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'author']

    def __str__(self):
        return self.user.username
