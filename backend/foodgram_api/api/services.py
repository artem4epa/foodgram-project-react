from datetime import datetime

from django.db.models import Sum
from recipes.models import RecipeIngredient


def create_shopping_cart(request, user):
    print(user)
    print()
    shopping_list = [
        f'Список покупок для: {user.first_name}\n'
    ]
    ingredients = RecipeIngredient.objects.filter(
        recipe__in_cart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).order_by('ingredient__name').annotate(amount=Sum('amount'))

    today = datetime.today()
    shopping_list = (
        f'Список покупок для: {user.first_name}\n\n'
        f'Дата: {today:%Y-%m-%d}\n\n'
    )
    shopping_list += '\n'.join([
        f'* {ingredient["ingredient__name"]} '
        f'({ingredient["ingredient__measurement_unit"]})'
        f' - {ingredient["amount"]}'
        for ingredient in ingredients
    ])
    shopping_list += f'\n\nFoodgram \n {today:%Y}'
    return shopping_list
