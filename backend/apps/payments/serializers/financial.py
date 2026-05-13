from rest_framework import serializers

from ..models import Coupon, FinancialAdjustment, Invoice, Payment, PaymentInstallment, Refund


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("academy",)


class PaymentInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInstallment
        fields = "__all__"
        read_only_fields = ("academy",)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("academy", "recorded_by", "payment_date")


class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    installments = PaymentInstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("academy", "balance_due", "status")


class FinancialAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAdjustment
        fields = "__all__"
        read_only_fields = ("academy", "approved_by")


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = "__all__"
        read_only_fields = ("academy", "requested_by", "status")
