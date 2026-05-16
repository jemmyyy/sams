from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.financial import (
    FinancialDashboardView,
    InvoiceViewSet,
    PaymentViewSet,
    RefundViewSet,
)

router = DefaultRouter()
router.register(r"invoices", InvoiceViewSet)
router.register(r"history", PaymentViewSet)
router.register(r"refunds", RefundViewSet)

app_name = "payments"

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", FinancialDashboardView.as_view(), name="financial_dashboard"),
]
