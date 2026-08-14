from datetime import date, datetime

from django.db import transaction

from apps.customer.domain.customer_number import generate_customer_number
from apps.customer.models import Customer, CustomerStatus, CustomerType


class CreateCustomerService:
    @staticmethod
    @transaction.atomic
    def execute(
        *,
        customer_type: CustomerType | str,
        first_name: str,
        last_name: str,
        middle_name: str | None = None,
        date_of_birth: date | str | None = None,
        email: str | None = None,  # <-- Ensure this is named 'email'
        phone_number: str | None = None,  # <-- Ensure this is named 'phone_number'
    ) -> Customer:
        # Extract string value if an Enum or Value Object was passed
        type_val = (
            customer_type.value
            if isinstance(customer_type, CustomerType)
            else customer_type
        )
        email_val = getattr(email, "value", email)
        phone_val = getattr(phone_number, "value", phone_number)

        # Standardize date format
        dob_val = date_of_birth
        if isinstance(date_of_birth, str) and date_of_birth.strip():
            try:
                dob_val = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                dob_val = datetime.strptime(date_of_birth, "%d-%m-%Y").date()

        return Customer.objects.create(
            customer_number=generate_customer_number(),
            customer_type=type_val,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            date_of_birth=dob_val,
            email=email_val,
            phone_number=phone_val,
            status=CustomerStatus.ACTIVE.value,
        )
