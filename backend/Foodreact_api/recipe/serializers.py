from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField

from users.serializers import UserSerializer
from .models import (
    Ingredient, Tag, Recipe,
    IngredientAmount, FavoriteRecipes,
    ShoppingCart
)


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер тагов."""

    class Meta:
        model = Tag
        fields = (
            'id', 'name',
            'color', 'slug'
        )

    def to_internal_value(self, data):
        if isinstance(data, int):
            get_object_or_404(Tag, id=data)
        else:
            raise serializers.ValidationError(
                f'Expect int, but got {type(data)}'
            )
        return data

    def validate(self, value):
        return value


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериалайзер ингридиент и количество."""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')

    def to_representation(self, instance):
        obj = instance.ingredient
        return {
            'id': obj.id,
            'name': obj.name,
            'measurement_unit': obj.measurement_unit,
            'amount': instance.amount
        }

    def validate(self, value):
        obj, _ = IngredientAmount.objects.get_or_create(
            ingredient=value.get('ingredient'),
            amount=value.get('amount')
        )
        return obj.pk


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер рецепта."""

    image = Base64ImageField()
    ingredients = IngredientAmountSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags',
            'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image',
            'text', 'cooking_time'
        )
        write_only = (
            'ingredients', 'tags'
            'image', 'name',
            'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and (
            user.author_favorite.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and (
            user.usercart.filter(recipe=obj).exists()
        )

    @staticmethod
    def __sep_m2m_data(validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        return validated_data, ingredients, tags

    def create(self, validated_data):
        validated_data, ingredients, tags = self.__sep_m2m_data(validated_data)
        instance = Recipe.objects.create(**validated_data)
        instance.ingredients.set(ingredients)
        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        validated_data, ingredients, tags = self.__sep_m2m_data(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.tags.set(tags)
        instance.ingredients.set(ingredients)
        instance.save()
        return instance


class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )


class SubscriptionSerializer(UserSerializer):
    """Сериалайзер подписок."""

    def to_representation(self, instance):
        limit_recipes = self.context.get(
            'request').query_params.get('limit_recipes')
        if limit_recipes is not None:
            limit_recipes = int(limit_recipes)
        user = instance
        recipes_obj = user.recipes.all()
        recipes = RecipesSerializer(
            recipes_obj[:limit_recipes], many=True,
            required=False)
        return {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_subscribed': True,
            'recipes': recipes.data,
            'recipes_count': recipes_obj.count()
        }


class FavoriteSerializer(serializers.ModelSerializer):
    '''Сериалайзер фаворитных рецептов.'''

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = FavoriteRecipes
        fields = (
            'author', 'recipe'
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=FavoriteRecipes.objects.all(),
                fields=['author', 'recipe']
            )
        ]

    def to_representation(self, instance):
        return RecipesSerializer(instance.recipe).data


class ShoppingCartSerializer(FavoriteSerializer):
    '''Сериалайзер покупательской корзины.'''

    class Meta:
        model = ShoppingCart
        fields = (
            'author', 'recipe'
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['author', 'recipe']
            )
        ]
