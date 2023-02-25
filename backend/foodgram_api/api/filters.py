from django.contrib.auth import get_user_model
import django_filters
from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = django_filters.filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(cart__user=user)
        return queryset
