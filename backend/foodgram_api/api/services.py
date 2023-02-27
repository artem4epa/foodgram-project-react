from recipes.models import RecipeIngredient
from django.db.models import Sum


def create_shopping_cart(request, user):
    shopping_list = [
        f'Список покупок для: {user.first_name}\n'
    ]
    ingredients = RecipeIngredient.objects.filter(
        recipe__in_cart__user=request.user
    ).values(
        'ingredients__name',
        'ingredients__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for ingredient in ingredients:
        shopping_list.append(
            f"{ingredient['indgredient__name']}:\
                {ingredient['amount']}\
                {ingredient['ingredient__measurement_unit']}"
        )
    return shopping_list
