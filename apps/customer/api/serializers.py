from rest_framework import serializers

from apps.accounts.api.serializers import AccountSerializer
from apps.customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            # Writable fields
            "customer_type",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
            "customer_number",
            "status",
            "updated_at",
            "accounts",
        ]

        read_only_fields = [
            "customer_number",
            "status",
            "updated_at",
        ]
