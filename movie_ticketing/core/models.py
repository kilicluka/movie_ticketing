import uuid

from django.db import models
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("UUID"),
        help_text=_("Instance's unique identifier."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("When was the instance created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("When was the instance updated."),
    )

    class Meta:
        abstract = True
