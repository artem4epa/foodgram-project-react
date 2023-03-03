from django.db.models import Sum
from recipes.models import RecipeIngredient


def create_shopping_cart(request, user):
    shopping_list = [
        f'Список покупок для: {user.first_name}\n'
    ]
    ingredient = RecipeIngredient.objects.filter(
        recipe__in_cart__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for ing in ingredient:
        shopping_list.append(
            f"{ing['indgredient__name']}:\
                {ing['amount']}\
                {ing['ingredient__measurement_unit']}"
        )
    return shopping_list
