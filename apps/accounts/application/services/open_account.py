from django.db import transaction

from apps.accounts.domain.account_number import generate_account_number
from apps.accounts.models import Account
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
        customer = Customer.objects.get(
            customer_number=customer_number,
            status="ACTIVE",
        )

        account = Account.objects.create(
            account_number=generate_account_number(),
            customer=customer,
            account_type=account_type,
            currency=currency,
        )

        return account
