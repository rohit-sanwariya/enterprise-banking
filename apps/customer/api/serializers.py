from rest_framework import serializers

from apps.customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "customer_type",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
        ]
