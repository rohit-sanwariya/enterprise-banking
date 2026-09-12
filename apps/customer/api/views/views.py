import logging

from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.customer.api.serializers import CustomerSerializer
from apps.customer.application.services.create_customer import (
    CreateCustomerService,
)
from apps.customer.models import Customer

logger = logging.getLogger(__name__)


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = (
        CustomerSerializer  # Changed from `serializer` to `serializer_class`
    )
    lookup_field = "customer_number"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = CreateCustomerService.execute(
            **serializer.validated_data,
        )

        return Response(
            self.get_serializer(customer).data,
            status=status.HTTP_201_CREATED,
        )
