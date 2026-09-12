from django.urls import path

from apps.customer.api.views.view import CustomerView

urlpatterns = [
    path(
        "",
        CustomerView.as_view(),
        name="create-customer",
    ),
]
