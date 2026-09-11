# apps/accounts/api/urls.py

from rest_framework.routers import DefaultRouter

from apps.accounts.views import AccountViewSet

router = DefaultRouter()

router.register("accounts", AccountViewSet, basename="account")

urlpatterns = router.urls
