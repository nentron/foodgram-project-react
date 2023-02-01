from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from users.views import (
    UserViewSet, TokenView,
)
from recipes.views import (
    IngredientViewset,
    TagViewset, RecipeViewset
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
    path(
        'api/docs/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    )
]
