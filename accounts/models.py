from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, email, username, display_name=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not display_name:
            display_name = username

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, display_name, password):
        user = self.create_user(
            email,
            username,
            display_name,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40)
    display_name = models.CharField(max_length=140)
    bio = models.TextField(max_length=140, blank=True, default="")
    avatar = models.ImageField(upload_to='avatar_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name", "username"]

    def __str__(self):
        return "{}".format(self.display_name)

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return "{} (@{})".format(self.display_name, self.username)

    def get_absolute_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.pk})


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    skill = models.ForeignKey(Skill, null=True, blank=True,
                              on_delete=models.CASCADE,
                              related_name='user_skill_relation')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_skill_relation')

    def __str__(self):
        return '{} - {}'.format(self.user.username,
                                self.skill.name)
