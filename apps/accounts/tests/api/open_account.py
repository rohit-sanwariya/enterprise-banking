import pytest
from rest_framework.test import APIClient

from apps.customer.models import Customer


@pytest.mark.django_db
def test_open_account_api():
    customer = Customer.objects.create(
        customer_number="CUS000001",
    )

    client = APIClient()

    response = client.post(
        "/api/v1/accounts/",
        {
            "customer_number": customer.customer_number,
            "account_type": "SAVINGS",
            "currency": "INR",
        },
        format="json",
    )

    assert response.status_code == 201

    assert response.data["account_number"] is not None
