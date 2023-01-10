from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import (
    UserViewSet, TokenObtainView,
    DestroyTokenView
)


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', TokenObtainView.as_view()),
    path('logout/', DestroyTokenView.as_view()),
]
