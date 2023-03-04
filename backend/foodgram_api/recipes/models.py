from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги'
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name'],),
        ]

    def __str__(self) -> str:
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False
    )
    measurement_unit = models.CharField(
        max_length=200,
        null=False
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name'],),
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Рецепт',
        max_length=200,
        help_text='Придумайте название рецепта',
    )
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='recipes',
        to=User,
        on_delete=models.SET_NULL,
        null=True,
    )
    tags = models.ManyToManyField(
        verbose_name='Тэг',
        related_name='recipes',
        to=Tag,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты блюда',
        related_name='recipes',
        through='recipes.RecipeIngredient',
    )
    pub_data = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )
    image = models.ImageField(
        verbose_name='Картинка готового блюда',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты',
        ordering = ('-pub_data',)
        indexes = [
            models.Index(fields=['-pub_data'],),
        ]

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        related_name='ingredient',
        to=Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        related_name='recipe',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        default=0,
        validators=(
            MinValueValidator(
                1
            ),
            MaxValueValidator(
                1000
            ),
        )
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe',)

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredient}'


class FavoriteRecipes(models.Model):
    recipe = models.ForeignKey(
        related_name='in_favorites',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        related_name='favorites',
        to=User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user', ],
                name='unique_recipe'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'


class Cart(models.Model):
    recipe = models.ForeignKey(
        related_name='in_cart',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        related_name='cart',
        to=User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe', ],
                name='uniq_cart_recipe'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'
