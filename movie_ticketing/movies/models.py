from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext as _


class Movie(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name=_("Title"),
        help_text=_("Title of the movie."),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description of the movie."),
    )

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        db_table = "movie"

    def __str__(self):
        return self.title
