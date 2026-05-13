from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.permissions.permissions import IsOperations, IsAdmin
from ..models import Invoice, Payment, Refund, FinancialAdjustment, Coupon
from ..serializers.financial import (
    InvoiceSerializer, PaymentSerializer, RefundSerializer, 
    FinancialAdjustmentSerializer, CouponSerializer
)
from ..services.financial import FinancialService
from ..tasks import export_financial_report

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsOperations]

    @action(detail=True, methods=['post'], url_path='record-payment')
    def record_payment(self, request, pk=None):
        invoice = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = FinancialService.record_payment(
                invoice=invoice,
                amount=serializer.validated_data['amount'],
                method=serializer.validated_data['method'],
                recorded_by=request.user,
                reference_number=serializer.validated_data.get('reference_number', ""),
                notes=serializer.validated_data.get('notes', "")
            )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='apply-adjustment')
    def apply_adjustment(self, request, pk=None):
        invoice = self.get_object()
        serializer = FinancialAdjustmentSerializer(data=request.data)
        if serializer.is_valid():
            adjustment = FinancialService.apply_adjustment(
                invoice=invoice,
                amount=serializer.validated_data['amount'],
                adjustment_type=serializer.validated_data['adjustment_type'],
                reason=serializer.validated_data['reason'],
                approved_by=request.user
            )
            return Response(FinancialAdjustmentSerializer(adjustment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOperations]

    @action(detail=True, methods=['post'], url_path='request-refund')
    def request_refund(self, request, pk=None):
        payment = self.get_object()
        serializer = RefundSerializer(data=request.data)
        if serializer.is_valid():
            refund = FinancialService.process_refund(
                payment=payment,
                amount=serializer.validated_data['amount'],
                reason=serializer.validated_data['reason'],
                requested_by=request.user,
                approved_by=request.user if request.user.is_superuser else None
            )
            return Response(RefundSerializer(refund).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'], url_path='receipt')
    def generate_receipt(self, request, pk=None):
        payment = self.get_object()
        receipt_data = FinancialService.generate_receipt(payment)
        return Response(receipt_data, status=status.HTTP_200_OK)

class FinancialDashboardView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        academy = request.user.academies.first() # In real RBAC, we get this from thread_local or active tenant
        report = FinancialService.get_receivables_report(academy)
        return Response({
            "success": True,
            "data": report
        })

    @action(detail=False, methods=['post'], url_path='export-report')
    def post(self, request):
        academy_id = request.user.academies.first().id
        export_financial_report.delay(academy_id, request.user.email)
        return Response({"status": "Export task initiated. You will receive an email shortly."}, status=status.HTTP_202_ACCEPTED)

