from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext as _


class UserProfile(BaseModel, AbstractBaseUser):
    USERNAME_FIELD = "email"

    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name=_("Email"),
        help_text=_("User's email."),
    )

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        db_table = "user_profile"
