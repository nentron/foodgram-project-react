import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers, response
from django.shortcuts import get_object_or_404


from users.serializers import UserSerializer
from users.models import Subscription
from .models import (
    Ingredient, Tag, Reciept,
    IngredientAmount, FavoriteReciepes
)


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
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

    def run_validation(self, data):
        value = self.to_internal_value(data)
        return value


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            info, image = data.split(';base64,')
            suffix = info.split('/')[-1]
            data = ContentFile(base64.b64decode(image), 'image.' + suffix)
        return super().to_internal_value(data)


class IngredientAmountSerializer(serializers.ModelSerializer):
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

    def run_validation(self, data):
        value = dict(self.to_internal_value(data))
        obj, _ = IngredientAmount.objects.get_or_create(
            ingredient=value.get('ingredient'),
            amount=value.get('amount')
        )
        return obj.pk


class RecieptSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientAmountSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reciept
        fields = (
            'id', 'tags',
            'author', 'ingredients',
            'name', 'image',
            'text', 'cooking_time'
        )
        write_only = (
            'ingredients', 'tags'
            'image', 'name',
            'text', 'cooking_time'
        )

    def __sep_m2m_data(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        return validated_data, ingredients, tags

    def create(self, validated_data):
        validated_data, ingredients, tags = self.__sep_m2m_data(validated_data)
        instance = Reciept.objects.create(**validated_data)
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
    class Meta:
        model = Reciept
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'subscriber', 'user'
        )

    def to_representation(self, instance):
        limit_recipes = self.context.get(
            'request').query_params.get('limit_recipes')
        if limit_recipes is not None:
            limit_recipes = int(limit_recipes)
        user = instance.user
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
    class Meta:
        model = FavoriteReciepes
        fields = (
            'author', 'reciept'
        )

    def to_representation(self, instance):
        recipes = RecipesSerializer(instance.reciept)
        return recipes.data
