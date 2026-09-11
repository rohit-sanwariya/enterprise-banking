# apps/common/models.py

from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(trash=False)


class TrashModel(models.Model):
    trash = models.BooleanField(default=False)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
