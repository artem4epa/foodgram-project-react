from django.db.models import F
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag  # Cart
from rest_framework import serializers  # status
from users.models import User


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}
        model = User

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()


class RecipeAbbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only = '__all__',


class PasswordUpdateSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class FollowSerializer(UserSerializer):
    recipes = RecipeAbbSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]
        read_only_fields = '__all__',

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = '__all__',
        model = Tag

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = '__all__',
        model = Ingredient

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.measurement_unit = validated_data.get(
            'measurement_unit',
            instance.measurement_unit
        )
        instance.save()
        return instance


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class ReciepSerializers(serializers.ModelSerializer):
    tags = TagSerializers(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        reads_only_fields = (
            'is_favorite',
            'is_in_shopping_cart',
        )
        model = Recipe

    def get_ingredients(sefl, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe: Recipe) -> bool:
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe) -> bool:
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return user.cart.filter(recipe=recipe).exists()

    # def is_cart_exists(self, request):
    #     user = request.user
    #     if not Cart.objects.filter(user=user.id).exists():
    #         return Response(
    #             status=status.HTTP_400_BAD_REQUEST)
