import uuid
from enum import Enum

from django.db import models

from apps.common.models import TimestampModel, TrashModel


# Standard Python Enums
class CustomerType(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    BUSINESS = "BUSINESS"


class CustomerStatus(Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    DORMANT = "DORMANT"
    FROZEN = "FROZEN"
    DECEASED = "DECEASED"


class Customer(TrashModel, TimestampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_number = models.CharField(max_length=20, unique=True, editable=False)

    # Pass enum values as tuple pairs: (member.value, member.name or custom label)
    customer_type = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value.title()) for tag in CustomerType],
        default=CustomerType.INDIVIDUAL.value,
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value.title()) for tag in CustomerStatus],
        default=CustomerStatus.ACTIVE.value,
    )

    class Meta:
        db_table = '"customer"."customer"'
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.customer_number})"
