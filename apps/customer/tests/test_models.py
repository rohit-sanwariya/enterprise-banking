import logging

import pytest

from apps.customer.models import Customer

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_create_customer():
    customer = Customer.objects.create(
        customer_number="CUST001",
        first_name="Rohit",
        last_name="Samaria",
        email="rohit@example.com",
    )

    # DB persistence
    assert customer.id is not None
    logger.info(f"{customer.id}abcd")
    # Default values
    assert customer.status == "ACTIVE"
    assert customer.customer_type == "INDIVIDUAL"
    logger.info(str(customer))
    # String representation
    assert str(customer) == "Rohit Samaria (CUST001)"


@pytest.mark.django_db
def test_update_customer():
    customer = Customer.objects.create(
        customer_number="CUST001",
        first_name="Rohit",
        last_name="Samaria",
        email="rohitsanwariya1995@gmail.com",
    )

    customer.customer_number = "CUST002"

    customer.save()
