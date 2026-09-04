import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customer.api.serializers import CustomerSerializer
from apps.customer.application.services.create_customer import (
    CreateCustomerService,
)
from apps.customer.models import Customer

logger = logging.getLogger(__name__)


class CustomerView(APIView):
    serializer = CustomerSerializer
    queryset = Customer.objects.all()

    def get(self, request):
        customers = Customer.objects.all()
        logger.info(self.queryset.values())
        serializer = CustomerSerializer(
            customers,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = CreateCustomerService.execute(
            **serializer.validated_data,
        )

        return Response(
            {
                "customer_number": customer.customer_number,
                "customer_type": customer.customer_type,
                "first_name": customer.first_name,
                "middle_name": customer.middle_name,
                "last_name": customer.last_name,
                "date_of_birth": customer.date_of_birth,
                "email": customer.email,
                "phone_number": customer.phone_number,
                "status": customer.status,
            },
            status=status.HTTP_201_CREATED,
        )
