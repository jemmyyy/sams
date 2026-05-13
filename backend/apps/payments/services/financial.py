from decimal import Decimal

from django.db import transaction
from django.db.models import Count, Q, Sum

from ..models import FinancialAdjustment, Invoice, Payment, Refund


class FinancialService:
    @staticmethod
    @transaction.atomic
    def record_payment(
        invoice: Invoice, amount: Decimal, method: str, recorded_by, reference_number="", notes=""
    ):
        """
        Records a manual payment (Cash/Bank Transfer) against an invoice.
        """
        payment = Payment.objects.create(
            academy=invoice.academy,
            invoice=invoice,
            amount=amount,
            method=method,
            recorded_by=recorded_by,
            reference_number=reference_number,
            notes=notes,
        )

        # Update invoice balance and status
        invoice.balance_due -= amount
        if invoice.balance_due <= 0:
            invoice.status = "paid"
            invoice.balance_due = Decimal("0.00")
        else:
            invoice.status = "partially_paid"

        invoice.save()

        # Check installments
        FinancialService._update_installments(invoice, amount)

        return payment

    @staticmethod
    def _update_installments(invoice: Invoice, paid_amount: Decimal):
        """
        Updates installment records as they are covered by payments.
        """
        remaining_to_apply = paid_amount
        installments = invoice.installments.filter(is_paid=False).order_by("due_date")

        for inst in installments:
            if remaining_to_apply >= inst.amount:
                inst.is_paid = True
                remaining_to_apply -= inst.amount
                inst.save()
            else:
                break

    @staticmethod
    @transaction.atomic
    def apply_adjustment(
        invoice: Invoice, amount: Decimal, adjustment_type: str, reason: str, approved_by
    ):
        """
        Applies a manual financial adjustment (Credit/Debit).
        """
        adjustment = FinancialAdjustment.objects.create(
            academy=invoice.academy,
            invoice=invoice,
            amount=amount,
            adjustment_type=adjustment_type,
            reason=reason,
            is_approved=True,
            approved_by=approved_by,
        )

        if adjustment_type == "credit":
            invoice.balance_due -= amount
        else:
            invoice.balance_due += amount
            invoice.total_amount += amount

        # Recalculate status
        if invoice.balance_due <= 0:
            invoice.status = "paid"
        elif invoice.balance_due < invoice.total_amount:
            invoice.status = "partially_paid"
        else:
            invoice.status = "unpaid"

        invoice.save()
        return adjustment

    @staticmethod
    @transaction.atomic
    def process_refund(
        payment: Payment, amount: Decimal, reason: str, requested_by, approved_by=None
    ):
        """
        Processes a refund for a specific payment.
        Requires approval if approved_by is None.
        """
        status = "approved" if approved_by else "pending"

        refund = Refund.objects.create(
            academy=payment.academy,
            payment=payment,
            amount=amount,
            reason=reason,
            status=status,
            requested_by=requested_by,
            approved_by=approved_by,
        )

        if status == "approved":
            # Reverse the payment effect on the invoice
            invoice = payment.invoice
            invoice.balance_due += amount

            # Recalculate status
            if invoice.balance_due >= invoice.total_amount:
                invoice.status = "unpaid"
            else:
                invoice.status = "partially_paid"

            invoice.save()

        return refund

    @staticmethod
    def generate_receipt(payment: Payment):
        """
        Generates a digital receipt for a payment.
        """
        return {
            "receipt_id": f"REC-{payment.id}",
            "date": payment.payment_date.isoformat(),
            "academy": payment.academy.name,
            "player": f"{payment.invoice.player.first_name} {payment.invoice.player.last_name}",
            "amount": str(payment.amount),
            "method": payment.get_method_display(),
            "reference": payment.reference_number,
            "invoice_id": payment.invoice.id,
            "remaining_balance": str(payment.invoice.balance_due),
        }

    @staticmethod
    def get_receivables_report(academy):
        """
        Aggregates financial data for dashboards.
        """
        return Invoice.objects.filter(academy=academy).aggregate(
            total_invoiced=Sum("total_amount"),
            total_outstanding=Sum("balance_due"),
            overdue_count=Count("id", filter=Q(status="overdue")),
        )
