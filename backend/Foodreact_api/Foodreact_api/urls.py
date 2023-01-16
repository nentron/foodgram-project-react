from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import (
    UserViewSet, TokenView,
)
from reciept.views import (
    IngredientViewset,
    TagViewset, RecieptViewset
)


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('auth/token', TokenView, basename='token')
router.register('ingredients', IngredientViewset, basename='ingredients')
router.register('tags', TagViewset, basename='tags')
router.register('reciepes', RecieptViewset, basename='reciepes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
