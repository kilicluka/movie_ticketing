from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from .managers import UserManager


class UserProfile(BaseModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"

    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name=_("Email"),
        help_text=_("User's email."),
    )
    is_staff = models.BooleanField(
        verbose_name=_("Is Staff"),
        default=False,
        help_text=_("Is user an admin user."),
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        db_table = "user_profile"

    def __str__(self):
        return self.email
