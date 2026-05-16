from apps.permissions.permissions import IsAdmin, IsOperations
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Invoice, Payment, Refund
from ..serializers.financial import (
    FinancialAdjustmentSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    RefundSerializer,
)
from ..services.financial import FinancialService
from ..tasks import export_financial_report


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsOperations]

    @action(detail=True, methods=["post"], url_path="record-payment")
    def record_payment(self, request, pk=None):
        invoice = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = FinancialService.record_payment(
                invoice=invoice,
                amount=serializer.validated_data["amount"],
                method=serializer.validated_data["method"],
                recorded_by=request.user,
                reference_number=serializer.validated_data.get("reference_number", ""),
                notes=serializer.validated_data.get("notes", ""),
            )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="apply-adjustment")
    def apply_adjustment(self, request, pk=None):
        invoice = self.get_object()
        serializer = FinancialAdjustmentSerializer(data=request.data)
        if serializer.is_valid():
            adjustment = FinancialService.apply_adjustment(
                invoice=invoice,
                amount=serializer.validated_data["amount"],
                adjustment_type=serializer.validated_data["adjustment_type"],
                reason=serializer.validated_data["reason"],
                approved_by=request.user,
            )
            return Response(
                FinancialAdjustmentSerializer(adjustment).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOperations]

    @action(detail=True, methods=["post"], url_path="request-refund")
    def request_refund(self, request, pk=None):
        payment = self.get_object()
        serializer = RefundSerializer(data=request.data)
        if serializer.is_valid():
            refund = FinancialService.process_refund(
                payment=payment,
                amount=serializer.validated_data["amount"],
                reason=serializer.validated_data["reason"],
                requested_by=request.user,
                approved_by=request.user if request.user.is_superuser else None,
            )
            return Response(RefundSerializer(refund).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="receipt")
    def generate_receipt(self, request, pk=None):
        payment = self.get_object()
        receipt_data = FinancialService.generate_receipt(payment)
        return Response(receipt_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.is_approved:
            return Response({"detail": "Payment already approved."}, status=status.HTTP_400_BAD_REQUEST)
        payment.approve(approved_by=request.user)
        return Response(PaymentSerializer(payment).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.is_approved:
            return Response({"detail": "Cannot reject an approved payment."}, status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get("reason", "")
        payment.reject(reason=reason, rejected_by=request.user)
        return Response(PaymentSerializer(payment).data)

    @action(detail=True, methods=["post"], url_path="reconcile")
    def reconcile_payment(self, request, pk=None):
        payment = self.get_object()
        if not payment.is_approved:
            return Response({"detail": "Cannot reconcile an unapproved payment."}, status=status.HTTP_400_BAD_REQUEST)
        if payment.reconciled:
            return Response({"detail": "Payment already reconciled."}, status=status.HTTP_400_BAD_REQUEST)
        FinancialService.reconcile_payment(payment, request.user)
        return Response(PaymentSerializer(payment).data)


class RefundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    permission_classes = [IsOperations]

    @action(detail=True, methods=["post"], url_path="approve")
    def approve_refund(self, request, pk=None):
        refund = self.get_object()
        if refund.status != "pending":
            return Response({"detail": "Only pending refunds can be approved."}, status=status.HTTP_400_BAD_REQUEST)
        refund.approve(approved_by=request.user)
        return Response(RefundSerializer(refund).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_refund(self, request, pk=None):
        refund = self.get_object()
        if refund.status != "pending":
            return Response({"detail": "Only pending refunds can be rejected."}, status=status.HTTP_400_BAD_REQUEST)
        refund.reject(rejected_by=request.user)
        return Response(RefundSerializer(refund).data)


class FinancialDashboardView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from apps.common.thread_local import get_current_academy_id
        from apps.academies.models import Academy

        academy_id = get_current_academy_id()
        academy = Academy.objects.get(pk=academy_id) if academy_id else None
        if not academy:
            return Response({"error": "Academy context required"}, status=status.HTTP_400_BAD_REQUEST)
        report = FinancialService.get_receivables_report(academy)
        reconciliation = FinancialService.get_reconciliation_report(academy)
        report.update(reconciliation)
        return Response({"success": True, "data": report})

    def post(self, request):
        from apps.common.thread_local import get_current_academy_id

        academy_id = get_current_academy_id()
        if not academy_id:
            return Response({"error": "Academy context required"}, status=status.HTTP_400_BAD_REQUEST)
        export_financial_report.delay(academy_id, request.user.email)
        return Response(
            {"status": "Export task initiated. You will receive an email shortly."},
            status=status.HTTP_202_ACCEPTED,
        )
