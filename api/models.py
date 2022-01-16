from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from uuid import uuid4

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name='Full Name',
        max_length=100,
        blank=True,
        null=True,
    )
    username = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(
        verbose_name='Date of Birth',
        blank=True, 
        null=True,
    )
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=10,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Check this option, instead of deleting the user.',
    )
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(
        default=False,
        help_text='Check if user is banned'
    )
    is_verified = models.BooleanField(
        default=False,
        help_text='Check if user is verified'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
