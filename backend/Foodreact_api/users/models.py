from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager
)


class CustomUserManager(UserManager):
    """Менеджер пользователя."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email requered')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('password required')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Абстрактный пользователь."""

    email = models.EmailField(
        verbose_name='Електронная почта',
        unique=True,
        blank=True
    )
    username = models.CharField('Логин',
                                blank=True,
                                max_length=255)
    subscriptions = models.ManyToManyField(
        to='self', through='Subscription',
        blank=True, related_name='following',
        symmetrical=False
    )
    objects = CustomUserManager()
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name'
    ]
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'user'
        ordering = ['-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def is_subscribed(self, sub):
        return sub in self.following.all()


class Subscription(models.Model):
    """Модель для формирования подписок."""

    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subber'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='usertosub'
    )

    class Meta:
        db_table = 'subscribe_users'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='Unque constrain', fields=('subscriber', 'user')
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('user')),
                name='You do not follow youself'
            )
        ]

    def __str__(self):
        return f'{self.user.email} - {self.subscriber.email}'
