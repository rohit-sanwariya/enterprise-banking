from django.urls import path

from apps.accounts.views import OpenAccountView

urlpatterns = [
    path("", OpenAccountView.as_view(), name="open-account"),
]
