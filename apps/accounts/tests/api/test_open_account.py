import pytest
from rest_framework.test import APIClient

from apps.customer.models import Customer


@pytest.mark.django_db
def test_open_account_api():
    client = APIClient()

    # Create customer through the real API
    customer_response = client.post(
        "/api/v1/customers/",
        {
            "customer_type": "INDIVIDUAL",
            "first_name": "Rohit",
            "last_name": "Sharma",
            "date_of_birth": "1995-05-15",
            "email": "rohit.sharma@example.com",
            "phone_number": "+919876543210",
        },
        format="json",
    )

    assert customer_response.status_code == 201

    customer_number = customer_response.data["customer_number"]

    assert Customer.objects.filter(
        customer_number=customer_number,
    ).exists()

    # Open account through the real API
    account_response = client.post(
        "/api/v1/accounts/",
        {
            "customer_number": customer_number,
            "account_type": "SAVINGS",
            "currency": "INR",
        },
        format="json",
    )

    assert account_response.status_code == 201

    # account_number = account_response.data["account_number"]
    #
    # assert account_number is not None
    #
    # # Verify account was persisted
    # assert Account.objects.filter(
    #     account_number=account_number,
    # ).exists()
