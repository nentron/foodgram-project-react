from rest_framework import pagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .mixins import CreateRetrieveListView
from .serializers import (
    UserSerializer, TokenSerializer,
    PasswordSetSerializer
)
from reciept.serializers import SubscriptionSerializer


User = get_user_model()


class UserViewSet(CreateRetrieveListView):
    """Вьюсет для пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(['post'], detail=False,
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = PasswordSetSerializer(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'],
            detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = request.user.following.all()
        results = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            instance=results, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.method == 'DELETE':
            request.user.following.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        request.user.following.add(user)
        serializer = SubscriptionSerializer(
            user, context={'request': request})
        return Response(
            serializer.data
        )


class TokenView(viewsets.ViewSet):
    """Вьюсет для получения/удаления токена."""

    @action(methods=['post'], name='create token',
            detail=False)
    def login(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(methods=['post'], name='delete token',
            permission_classes=[IsAuthenticated], detail=False)
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
