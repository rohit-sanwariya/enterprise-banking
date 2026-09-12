# apps/customer/api/urls.py
from rest_framework.routers import DefaultRouter

from apps.customer.api.views import CustomerView

router = DefaultRouter()
router.register(r"", CustomerView, basename="customer")

urlpatterns = router.urls
