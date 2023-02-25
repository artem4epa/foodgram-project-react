from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from django.core.exceptions import ObjectDoesNotExist


class CustomChecking:
    def check_and_add(self, model, user, pk, serializer):
        if model.objects.filter(user_id=user.id, recipe_id=pk).exists():
            return Response(
                {'errors': 'Этот рецепт уже добавлен.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = serializer(recipe)
        model.objects.create(recipe=recipe, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def check_and_delete(self, model, user, pk, serializer):
        try:
            recipe = get_object_or_404(Recipe, id=pk)
            serializer = serializer(recipe)
            model.objects.get(recipe=recipe, user=user).delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(
                {'errors': 'Такого рецепта не существует в Вашем списке.'},
                status=status.HTTP_400_BAD_REQUEST
            )
