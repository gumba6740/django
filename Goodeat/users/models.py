from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from config.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError('이메일이 필요합니다')
        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(email, password, *args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='users/profile_images', default='default/profile_default.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email