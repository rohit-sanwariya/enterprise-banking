from rest_framework import serializers

from apps.accounts.models import AccountType


class OpenAccountSerializer(serializers.Serializer):
    customer_number = serializers.CharField(required=True)
    account_type = serializers.ChoiceField(choices=AccountType.choices())
    currency = serializers.CharField(max_length=3, default="INR")

    @staticmethod
    def validate_currency(value: str):
        return value.upper()
