from django.db import models
from django.utils.translation import gettext as _


class ReservationStatus(models.TextChoices):
    OPEN = "OPEN", _("Open")
    COMPLETED = "COMPLETED", _("Completed")


class MovieFormat(models.TextChoices):
    TWO_D = "2D", _("2D")
    THREE_D = "3D", _("3D")
    FOUR_D_X = "4DX", _("4DX")
