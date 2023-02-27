from django.contrib import admin
from django.contrib.admin import display
from recipes.models import (Cart, FavoriteRecipes, Ingredient, Recipe,
                            RecipeIngredient, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_to_favorites')
    readonly_fields = ('added_to_favorites',)
    list_filter = ('author', 'name', 'tags',)

    @display(description='Number of favorites')
    def added_to_favorites(self, obj):
        return obj.in_favorites.count()


@admin.register(FavoriteRecipes)
class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredient(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount',)
