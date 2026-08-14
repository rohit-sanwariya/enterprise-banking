from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.api.serializers import OpenAccountSerializer
from apps.accounts.application.services.open_account import OpenAccountService
from apps.accounts.domain.exceptions.account_exists import AccountAlreadyExistsError
from apps.accounts.domain.exceptions.customer_does_not_exist import (
    CustomerNotFoundError,
)


class OpenAccountView(APIView):
    def post(self, request):
        serializer = OpenAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            account = OpenAccountService.execute(
                **serializer.validated_data,
            )
        except CustomerNotFoundError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AccountAlreadyExistsError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            {
                "id": str(account.id),
                "account_number": account.account_number,
                "customer_number": account.customer.customer_number,
                "account_type": account.account_type,
                "status": account.status,
                "currency": account.currency,
                "opened_at": account.opened_at,
            },
            status=status.HTTP_201_CREATED,
        )
