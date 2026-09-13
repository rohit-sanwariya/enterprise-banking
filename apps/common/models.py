# apps/common/models.py

import uuid

from django.db import models
from django.utils import timezone


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveQuerySet(models.QuerySet):
    def delete(self):
        """Soft-delete all items in queryset (bulk operations)."""
        return self.update(trash=True, trashed_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all items in queryset from DB."""
        return super().delete()

    def restore(self):
        """Restore all soft-deleted items in queryset."""
        return self.update(trash=False, trashed_at=None)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db).filter(trash=False)


class TrashModel(models.Model):
    trash = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()  # Returns only non-trashed records
    all_objects = models.Manager()  # Returns everything (including trashed)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete single model instance."""
        self.trash = True
        self.trashed_at = timezone.now()
        self.save(update_fields=["trash", "trashed_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete single instance from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore soft-deleted instance."""
        self.trash = False
        self.trashed_at = None
        self.save(update_fields=["trash", "trashed_at"])


class OutboxEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event_type = models.CharField(max_length=255)

    payload = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    published = models.BooleanField(default=False)

    class Meta:
        db_table = "outbox_events"
        indexes = [
            models.Index(fields=["published", "created_at"]),
        ]
