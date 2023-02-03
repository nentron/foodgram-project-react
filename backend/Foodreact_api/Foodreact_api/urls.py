from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi, views

from users.views import (
    UserViewSet, TokenView,
)
from recipes.views import (
    IngredientViewset,
    TagViewset, RecipeViewset
)


schema_view = views.get_schema_view(
    openapi.Info(
        title='FoodGram Api',
        default_version='v1',
        description='Api документация для Foodgram'
    ),
    public=True
)


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('auth/token', TokenView, basename='token')
router.register('ingredients', IngredientViewset, basename='ingredients')
router.register('tags', TagViewset, basename='tags')
router.register('recipes', RecipeViewset, basename='recipes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(
        r'^redoc/$', schema_view.with_ui(
            'redoc', cache_timeout=0
        ),
        name='schema-redoc'
    )
]
