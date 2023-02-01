from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from users.views import (
    UserViewSet, TokenView,
)
from recipes.views import (
    IngredientViewset,
    TagViewset, RecipeViewset
)


schema_view = get_schema_view(title='FoodGram')


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('auth/token', TokenView, basename='token')
router.register('ingredients', IngredientViewset, basename='ingredients')
router.register('tags', TagViewset, basename='tags')
router.register('recipes', RecipeViewset, basename='recipes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(
        'openapi',
        schema_view,
        name='openapi-schema'
    ),
    path(
        'api/docs/',
        TemplateView.as_view(
            template_name='redoc.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='redoc'
    )
]
