# apps/customer/infrastructure/models.py
import uuid

from django.db import models


class CustomerModel(models.Model):
    """Django ORM model for Customer persistence."""

    # Identity — matches domain entity
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_number = models.CharField(max_length=20, unique=True, editable=False)

    # Customer type — store as string
    customer_type = models.CharField(
        max_length=20,
        choices=[
            ("INDIVIDUAL", "Individual"),
            ("BUSINESS", "Business"),
        ],
        default="INDIVIDUAL",
    )

    # Personal info
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    # Contact — store as string (value objects handled in repository)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Status — store as string
    status = models.CharField(
        max_length=20,
        choices=[
            ("ACTIVE", "Active"),
            ("CLOSED", "Closed"),
            ("DORMANT", "Dormant"),
            ("FROZEN", "Frozen"),
            ("DECEASED", "Deceased"),
        ],
        default="ACTIVE",
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_number} - {self.first_name} {self.last_name}"
