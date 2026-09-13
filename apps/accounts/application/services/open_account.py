from django.db import transaction

from apps.accounts.domain.account_number import generate_account_number
from apps.accounts.domain.exceptions.account_exists import AccountAlreadyExistsError
from apps.accounts.domain.exceptions.customer_does_not_exist import (
    CustomerNotFoundError,
)
from apps.accounts.models import Account
from apps.common.models import OutboxEvent
from apps.customer.models import Customer


class OpenAccountService:
    @staticmethod
    @transaction.atomic
    def execute(
        *,
        customer_number: str,
        account_type: str,
        currency: str = "INR",
    ) -> Account:

        try:
            customer = Customer.objects.get(
                customer_number=customer_number,
            )
        except Customer.DoesNotExist as err:
            raise CustomerNotFoundError(f"{customer_number} does not exist") from err

        if Account.objects.filter(
            customer=customer,
            account_type=account_type,
        ).exists():
            raise AccountAlreadyExistsError(
                f"{account_type} for {customer_number} already exists"
            )

        account = Account.objects.create(
            account_number=generate_account_number(),
            customer=customer,
            account_type=account_type,
            currency=currency,
        )

        OutboxEvent.objects.create(
            event_type="account.created",
            payload={
                "account_id": str(account.id),
                "customer_id": str(customer.id),
                "email": customer.email,
            },
        )

        return account
