from django.db import models
from django.utils import timezone


class ShowtimeManager(models.Manager):
    def showing(self):
        return self.get_queryset().filter(time_showing__gt=timezone.now())
