from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField('Название', max_length=255)
    measurement_unit = models.CharField('Ед. измерения', max_length=10)

    class Meta:
        db_table = 'ingredient'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}-{self.measurement_unit}'


class IngredientAmount(models.Model):
    """Модель ингредиент и количество."""

    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        db_table = 'ingredient_amount'
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient}:{self.amount}'


class Tag(models.Model):
    """Модель тагов."""

    name = models.CharField('Название', max_length=70)
    color = models.CharField('Hex-цвет', max_length=30)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        db_table = 'tags'
        verbose_name = 'Таг'
        verbose_name_plural = 'Таги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField('Название', max_length=255)
    image = models.ImageField('Картинка', upload_to='recipes/images/')
    text = models.TextField('Текст')
    ingredients = models.ManyToManyField(
        IngredientAmount
    )
    tags = models.ManyToManyField(Tag, blank=False)
    created = models.DateField('Время создания', auto_now=True)
    cooking_time = models.PositiveIntegerField('Время готовки, минуты',
                                               null=True)

    class Meta:
        db_table = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created']

    def __str__(self):
        return f'Aвтор: {self.author}, название рецепта: {self.name}'


class ShoppingCart(models.Model):
    """Модель корзины."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='usercart'
    )
    recipe = models.ForeignKey(
        Recipe, related_name='recipe_to_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'shopping_cart'
        constraints = [
            models.UniqueConstraint(
                name='Unque shoppingcart', fields=('author', 'recipe')
            ),
        ]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.author} - {self.recipe__name}'


class FavoriteRecipes(models.Model):
    """Модель фаворитных рецептов."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author_favorite'
    )
    recipe = models.ForeignKey(
        Recipe, related_name='recipe_to_favorite',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'favorite_recipes'
        constraints = [
            models.UniqueConstraint(
                name='Unque favorite', fields=('author', 'recipe')
            ),
        ]
        verbose_name = 'Фаворитный'
        verbose_name_plural = 'Фаворитные'

    def __str__(self):
        return f'{self.author} - {self.recipe__name}'
