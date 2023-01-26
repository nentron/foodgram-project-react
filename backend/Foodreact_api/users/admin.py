from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    """Модель админпанели пользователей."""

    empty_value_display = 'empty'
    list_display = ['email', 'username']
    list_filter = ['email', 'username']
    search_fields = ['email', 'username']


admin.site.register(Subscription)
