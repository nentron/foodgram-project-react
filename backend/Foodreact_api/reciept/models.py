from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=10)


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=70)
    color = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)


class Reciept(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='reciepes/images/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        IngredientAmount
    )
    tags = models.ManyToManyField(Tag)
    created = models.DateField(auto_now=True)
    cooking_time = models.PositiveIntegerField(null=True)
