from django.db.models import F, Sum
from recipes.models import RecipeIngredient


def create_shopping_cart(request, user):
    shopping_list = [
        f'Список покупок для: {user.first_name}\n'
    ]
    ingredients = RecipeIngredient.objects.filter(
        recipe__in_cart__user=request.user
    ).values(
        'ingredient__name',
        measurement=F('ingredient__measurement_unit')
    ).annotate(amount=Sum('ingredient__amount'))
    print(ingredients)
    for ingredient in ingredients:
        shopping_list.append(
            f"{ingredient['ingredient__name']}"
            f"{ingredient['amount']}"
            f"{ingredient['measurement']}"
        )
    return shopping_list
