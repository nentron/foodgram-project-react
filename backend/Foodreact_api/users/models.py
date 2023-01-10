from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager
)


class CustomUserManager(UserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an emaila address')
        if not password:
            raise ValueError('Password required')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        blank=True
    )
    username = models.CharField(blank=True,
                                max_length=255)
    is_subscribed = models.BooleanField(
        default=False
    )
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
