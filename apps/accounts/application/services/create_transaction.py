from decimal import Decimal

from django.db import transaction

from apps.accounts.models import Account, Transaction
from apps.customer.domain.enums.transaction_type import TransactionType


class CreateTransactionService:
    @staticmethod
    @transaction.atomic
    def execute(
        *,
        account_number: str,
        transaction_type: TransactionType,
        amount: Decimal,
    ) -> Transaction:

        account = Account.objects.select_for_update().get(account_number=account_number)
        if transaction_type == TransactionType.DEBIT:
            balance_after = account.balance - Decimal(amount)
            if balance_after < 0:
                raise ValueError("Insufficient balance")
        elif transaction_type == TransactionType.CREDIT:
            balance_after = account.balance + Decimal(amount)
        else:
            raise ValueError("Invalid transaction type")
        account.balance = balance_after
        account.save(update_fields=["balance", "updated_at"])
        return Transaction.objects.create(
            account=account,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=balance_after,
        )
