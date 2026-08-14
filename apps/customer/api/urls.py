from django.urls import path

from apps.customer.api.views.create_customer_view import CreateCustomerView

urlpatterns = [
    path(
        "",
        CreateCustomerView.as_view(),
        name="create-customer",
    ),
]
