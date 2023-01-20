from django.contrib import admin

from .models import User
from reciept.models import (
    Reciept, IngredientAmount,
    Ingredient, Tag
)


class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['email', 'username']
    list_filter = ['email', 'username']
    search_fields = ['email', 'username']


class RecieptAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ['author', 'name', 'tags']


admin.site.register(User, AuthorAdmin)
admin.site.register(Reciept, RecieptAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Tag)
