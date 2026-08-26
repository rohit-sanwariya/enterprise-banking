import uuid
from collections.abc import Sequence
from enum import Enum
from typing import Any

from django.db import models
from django.db.models import Q

from apps.customer.domain.enums.transaction_type import TransactionType


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

    balance = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0,
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
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "account_type"],
                name="uq_account_customer_type",
            ),
            models.CheckConstraint(
                condition=Q(balance__gte=0),
                name="account_balance_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return self.account_number


class Transaction(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )

    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
    )

    balance_after = models.DecimalField(
        max_digits=19,
        decimal_places=2,
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = '"accounts"."transaction"'
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="transaction_amount_positive",
            ),
            models.CheckConstraint(
                condition=Q(balance_after__gte=0),
                name="transaction_balance_after_non_negative",
            ),
        ]
