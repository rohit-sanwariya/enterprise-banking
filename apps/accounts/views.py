from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.api.serializers import OpenAccountSerializer
from apps.accounts.application.services.open_account import OpenAccountService


class OpenAccountView(APIView):
    def post(self, request):
        serializer = OpenAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = OpenAccountService.execute(
            **serializer.validated_data,
        )

        return Response(
            {
                "id": account.id,
                "account_number": account.account_number,
                "customer_id": account.customer_id,
                "account_type": account.account_type,
                "status": account.status,
                "currency": account.currency,
                "opened_at": account.opened_at,
            },
            status=status.HTTP_201_CREATED,
        )
