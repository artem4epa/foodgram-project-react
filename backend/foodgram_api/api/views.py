from rest_framework import viewsets, status
from recipes.models import (
    Tag, Recipe, Ingredient, Cart, RecipeIngredient, FavoriteRecipes
)
from api.serializers import (
    TagSerializers, IngredientSerializers, ReciepSerializers,
    FollowSerializer, RecipeAbbSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import AdminOrReadOnly, AuthorAdminsOrReadOnly
from django.contrib.auth import get_user_model
from api.paginators import CustomPagination
from api.checking import CustomChecking
from django.db.models import Sum
from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import IngredientFilter, RecipeFilter


User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = [AdminOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet, CustomChecking):
    queryset = Recipe.objects.select_related('author')
    serializer_class = ReciepSerializers
    permission_classes = [AuthorAdminsOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete', ],
        detail=True,
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.check_and_add(
                Cart,
                request.user,
                pk,
                RecipeAbbSerializer
            )
        return self.check_and_delete(
            Cart,
            request.user.id,
            pk,
            RecipeAbbSerializer
        )

    @action(
        methods=['GET', ],
        detail=False,
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not Cart.objects.filter(user=user.id).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        filename = f'{user.username}_shopping_list.pdf'
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
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        methods=['post', 'delete', ],
        detail=True,
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.check_and_add(
                FavoriteRecipes,
                request.user,
                pk,
                RecipeAbbSerializer
            )
        return self.check_and_delete(
            FavoriteRecipes,
            request.user,
            pk,
            RecipeAbbSerializer
        )


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        methods=['post', 'delete'],
        url_path=r'(?P<id>\d+)/subscribe',
        url_name='subscribe'
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            author, context={'request': self.request}
        )
        if request.method == 'POST':
            self.request.user.subscribe.add(author)
            print(self.request.user)
            print(serializer.data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.request.user.subscribe.remove(author)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
        )
        return self.get_paginated_response(serializer.data)
