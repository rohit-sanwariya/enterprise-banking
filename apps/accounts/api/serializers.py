from rest_framework import serializers

from apps.accounts.models import AccountType
from apps.customer.domain.enums.transaction_type import TransactionType


class OpenAccountSerializer(serializers.Serializer):
    customer_number = serializers.CharField(required=True)
    account_type = serializers.ChoiceField(choices=AccountType.choices())
    currency = serializers.CharField(max_length=3, default="INR")

    @staticmethod
    def validate_currency(value: str):
        return value.upper()


class CreateTransactionSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(choices=TransactionType.choices())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
