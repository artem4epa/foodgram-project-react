from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (RecipeViewSet, TagViewSet,
                    IngredientViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'tags', TagViewSet, 'tags')
router.register(r'recipes', RecipeViewSet, 'recipes')
router.register(r'ingredients', IngredientViewSet, 'ingredients')


app_name = 'api'

urlpatterns = [
     path('', include(router.urls)),
     path('auth/', include('djoser.urls.authtoken')),
]
