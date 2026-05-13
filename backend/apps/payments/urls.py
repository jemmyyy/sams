from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.financial import InvoiceViewSet, PaymentViewSet, FinancialDashboardView

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'history', PaymentViewSet)

app_name = 'payments'

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', FinancialDashboardView.as_view(), name='financial_dashboard'),
]
