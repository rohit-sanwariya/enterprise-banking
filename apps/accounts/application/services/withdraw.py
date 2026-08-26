from decimal import Decimal

from django.db import transaction

from apps.accounts.models import Account, Transaction
from apps.customer.domain.enums.transaction_type import TransactionType


class WithdrawService:
    @staticmethod
    @transaction.atomic
    def execute(
        *,
        account_number: str,
        amount: Decimal,
    ) -> Transaction:
        account = Account.objects.select_for_update().get(account_number=account_number)
        if amount < 0:
            raise ValueError("Invalid amount")
        balance_after = account.balance - amount
        if balance_after < 0:
            raise ValueError("Insufficient balance")
        account.balance = balance_after
        account.save()

        return Transaction(
            account=account,
            transaction_type=TransactionType.DEBIT,
            amount=amount,
            balance=balance_after,
        )
