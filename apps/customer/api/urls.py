from django.urls import path

from apps.customer.api.views.create_customer_view import CustomerView

urlpatterns = [
    path(
        "",
        CustomerView.as_view(),
        name="create-customer",
    ),
]
