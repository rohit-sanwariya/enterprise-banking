import pytest
from rest_framework.test import APIClient

from apps.customer.models import Customer


@pytest.mark.django_db
def test_create_customer_api():
    client = APIClient()

    payload = {
        "customer_type": "INDIVIDUAL",
        "first_name": "Rohit",
        "middle_name": "",
        "last_name": "Sharma",
        "date_of_birth": "1995-05-15",
        "email": "rohit.sharma@example.com",
        "phone_number": "+919876543210",
    }

    response = client.post(
        "/api/v1/customers/",
        payload,
        format="json",
    )

    assert response.status_code == 201

    assert response.data["customer_number"].startswith("CUS")
    assert response.data["customer_type"] == "INDIVIDUAL"
    assert response.data["first_name"] == "Rohit"
    assert response.data["last_name"] == "Sharma"

    customer = Customer.objects.get(customer_number=response.data["customer_number"])

    assert customer.first_name == "Rohit"
    assert customer.last_name == "Sharma"
    assert customer.email == "rohit.sharma@example.com"
    assert customer.phone_number == "+919876543210"
    assert customer.status == "ACTIVE"
