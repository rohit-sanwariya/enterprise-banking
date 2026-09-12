from rest_framework.viewsets import ModelViewSet

from apps.accounts.api.serializers import (
    AccountDetailSerializer,
    AccountSerializer,
    AccountUpdateSerializer,
    OpenAccountSerializer,
)
from apps.accounts.models import Account


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    lookup_field = "account_number"

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only perform the JOIN with Customer when fetching a single detail record
        if self.action == "retrieve":
            return queryset.select_related("customer")
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return OpenAccountSerializer
        elif self.action in ["update", "partial_update"]:
            return AccountUpdateSerializer
        elif self.action == "retrieve":
            return AccountDetailSerializer
        # Default for 'list' and other actions
        return AccountSerializer
