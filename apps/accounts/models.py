import uuid
from collections.abc import Sequence
from enum import Enum
from typing import Any

from django.db import models


# Standard Python Enums
class AccountType(Enum):
    SAVINGS = "SAVINGS"
    CURRENT = "CURRENT"

    @classmethod
    def choices(cls) -> Sequence[Any]:
        return [(tag.value, tag.value.title()) for tag in cls]


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class Account(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    account_number = models.CharField(
        max_length=20,
        unique=True,
    )

    # References Customer model in the customer app
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.PROTECT,
        related_name="accounts",
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices(),
    )

    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value.title()) for tag in AccountStatus],
        default=AccountStatus.ACTIVE.value,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    opened_at = models.DateTimeField(
        auto_now_add=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = '"accounts"."account"'
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.account_number
