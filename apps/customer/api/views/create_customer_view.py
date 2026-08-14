from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customer.api.serializers import CreateCustomerSerializer
from apps.customer.application.services.create_customer import (
    CreateCustomerService,
)


class CreateCustomerView(APIView):
    def post(self, request):
        serializer = CreateCustomerSerializer(data=request.data)
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
