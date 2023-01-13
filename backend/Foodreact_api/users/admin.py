from django.contrib import admin

from .models import User
from reciept.models import (
    Reciept, IngredientAmount,
    Ingredient, Tag
)

admin.site.register(User)
admin.site.register(Reciept)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Tag)
