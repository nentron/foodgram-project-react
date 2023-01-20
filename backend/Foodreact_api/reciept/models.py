from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=10)

    def __str__(self):
        return '{0}-{1}'.format(self.name, self.measurement_unit)


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return '{0}:{1}'.format(self.ingredient, self.amount)


class Tag(models.Model):
    name = models.CharField(max_length=70)
    color = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Reciept(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='reciepes/images/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        IngredientAmount
    )
    tags = models.ManyToManyField(Tag)
    created = models.DateField(auto_now=True)
    cooking_time = models.PositiveIntegerField(null=True)


class ShoppingCart(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='usercart'
    )
    reciept = models.ForeignKey(
        Reciept, related_name='reciept_to_cart',
        on_delete=models.CASCADE
    )


class FavoriteReciepes(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author_favorite'
    )
    reciept = models.ForeignKey(
        Reciept, related_name='reciept_to_favorite',
        on_delete=models.CASCADE
    )
