from decimal import Decimal

from apps.common.models import TenantAwareModel
from django.core.validators import MinValueValidator
from django.db import models


class Coupon(TenantAwareModel):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code


class Discount(TenantAwareModel):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]
    name = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.discount_type}: {self.value})"


class Invoice(TenantAwareModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("unpaid", "Unpaid"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("void", "Void"),
    ]

    player = models.ForeignKey("players.Player", on_delete=models.PROTECT, related_name="invoices")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices")
    description = models.TextField()
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    balance_due = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpaid")

    # Track metadata
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "due_date"]),
        ]

    def __str__(self):
        return f"Invoice {self.id} - {self.player} - {self.total_amount}"


class PaymentInstallment(TenantAwareModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="installments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["due_date"]


class Payment(TenantAwareModel):
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("other", "Other"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    reference_number = models.CharField(
        max_length=100, blank=True, help_text="Transaction ID, Check #, etc."
    )
    recorded_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="recorded_payments"
    )

    # Approval workflow
    is_approved = models.BooleanField(
        default=False
    )
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_payments",
    )

    reconciled = models.BooleanField(default=False)
    reconciled_at = models.DateTimeField(null=True, blank=True)
    reconciled_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reconciled_payments",
    )
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.method == "cash" and self._state.adding:
            self.is_approved = True
        super().save(*args, **kwargs)

    def approve(self, approved_by):
        if self.is_approved:
            return
        self.is_approved = True
        self.approved_by = approved_by
        self.save(update_fields=["is_approved", "approved_by"])

    def reject(self, reason, rejected_by):
        if self.is_approved:
            return
        self.notes = f"{self.notes}\nRejected by {rejected_by}: {reason}".strip()
        self.save(update_fields=["notes"])

    def __str__(self):
        return f"Payment {self.id} - {self.amount} via {self.method}"


class Refund(TenantAwareModel):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="refunds")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending",
    )
    requested_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="requested_refunds"
    )
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_refunds",
    )

    def approve(self, approved_by):
        if self.status != "pending":
            return
        self.status = "approved"
        self.approved_by = approved_by
        self.save(update_fields=["status", "approved_by"])

    def reject(self, rejected_by):
        if self.status != "pending":
            return
        self.status = "rejected"
        self.approved_by = rejected_by
        self.save(update_fields=["status", "approved_by"])


class LateFee(TenantAwareModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="late_fees")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255, default="Late Payment Penalty")


class FinancialAdjustment(TenantAwareModel):
    ADJUSTMENT_TYPES = [
        ("credit", "Credit (Decrease Balance)"),
        ("debit", "Debit (Increase Balance)"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="adjustments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True
    )
