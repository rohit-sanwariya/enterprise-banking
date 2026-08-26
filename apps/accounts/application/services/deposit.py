from decimal import Decimal

from django.db import transaction

from apps.accounts.application.services.create_transaction import (
    CreateTransactionService,
)
from apps.accounts.models import Account, Transaction
from apps.customer.domain.enums.transaction_type import TransactionType


class DepositService:
    @staticmethod
    @transaction.atomic
    def execute(
        *,
        account_number: str,
        amount: Decimal,
    ) -> Transaction:

        if amount < 0:
            raise ValueError("Amount must be positive")

        account = Account.objects.select_for_update().get(account_number=account_number)

        balance_after = account.balance + amount
        account.balance = balance_after
        account.save(update_fields=("balance", "updated_at"))

        return CreateTransactionService.execute(
            account_number=account_number,
            amount=amount,
            transaction_type=TransactionType.CREDIT,
        )
