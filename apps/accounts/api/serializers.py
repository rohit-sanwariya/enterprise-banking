from rest_framework import serializers

from apps.accounts.application.services.open_account import OpenAccountService
from apps.accounts.domain.exceptions.account_exists import AccountAlreadyExistsError
from apps.accounts.domain.exceptions.customer_does_not_exist import (
    CustomerNotFoundError,
)
from apps.accounts.models import Account, AccountType
from apps.customer.domain.enums.transaction_type import TransactionType
from apps.customer.models import Customer


class OpenAccountSerializer(serializers.Serializer):
    customer_number = serializers.CharField(required=True)
    account_type = serializers.ChoiceField(choices=AccountType.choices())
    currency = serializers.CharField(max_length=3, default="INR")

    def create(self, validated_data):
        try:
            return OpenAccountService.execute(**validated_data)
        except CustomerNotFoundError as exc:
            raise serializers.ValidationError({"customer_number": str(exc)}) from None
        except AccountAlreadyExistsError as exc:
            raise serializers.ValidationError({"detail": str(exc)}) from None

    def to_representation(self, instance):
        """
        Delegates response serialization to AccountSerializer,
        preventing 'Account object has no attribute customer_number' errors.
        """
        return AccountSerializer(instance, context=self.context).data

    @staticmethod
    def validate_currency(value: str):
        return value.upper()


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["account_type", "currency"]  # 'customer' is completely omitted


class CustomerSummarySerializer(serializers.ModelSerializer):
    """Lightweight representation used strictly for embedding in Account details."""

    class Meta:
        model = Customer
        fields = ["customer_number", "first_name", "last_name", "email", "phone_number"]


class AccountDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with full customer details for detail view."""

    customer = CustomerSummarySerializer(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "account_number",
            "customer",  # Nested Customer object
            "account_type",
            "status",
            "currency",
            "balance",
            "created_at",
            "updated_at",
        ]


class CreateTransactionSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(choices=TransactionType.choices())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_number",
            "customer",
            "account_type",
            "status",
            "currency",
            "balance",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "account_number",
            "status",
            "balance",
            "created_at",
            "updated_at",
        ]
