from django.contrib import admin

from recipe.models import (
    Recipe, IngredientAmount,
    Ingredient, Tag
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель адимнпанели рецептов."""

    readonly_fields = ('count_favorite',)
    list_display = ['name', 'author']
    list_filter = ['author', 'name', 'tags']
    search_fields = ['author__email', 'name', 'tags__name']

    @admin.display(description='Favorite count')
    def count_favorite(self, obj):
        return obj.recipe_to_favorite.all().count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель админпанели ингредиентов."""

    list_display = ['name', 'measurement_unit']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(IngredientAmount)
admin.site.register(Tag)
