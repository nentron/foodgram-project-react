from django.contrib import admin

from .models import User
from reciept.models import (
    Reciept, IngredientAmount,
    Ingredient, Tag
)


class AuthorAdmin(admin.ModelAdmin):
    '''Модель админпанели пользователей.'''

    empty_value_display = 'empty'
    list_display = ['email', 'username']
    list_filter = ['email', 'username']
    search_fields = ['email', 'username']


class RecieptAdmin(admin.ModelAdmin):
    '''Модель адимнпанели рецептов.'''

    readonly_fields = ('count_favorite',)
    list_display = ['name', 'author']
    list_filter = ['author', 'name', 'tags']
    search_fields = ['author__email', 'name', 'tags__name']

    @admin.display(description='Favorite count')
    def count_favorite(self, obj):
        return obj.reciept_to_favorite.all().count()


class IngredientAdmin(admin.ModelAdmin):
    '''Модель админпанели ингредиентов.'''

    list_display = ['name', 'measurement_unit']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(User, AuthorAdmin)
admin.site.register(Reciept, RecieptAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(Tag)
