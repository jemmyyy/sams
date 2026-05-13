# SAMS Offline Financial System Strategy

## Financial Consistency Strategy
Financial integrity is guaranteed through the strict use of Django's `@transaction.atomic` on all mutating operations (e.g., `record_payment`, `apply_adjustment`, `process_refund`). This ensures that an invoice's `balance_due` and `status` are perfectly synchronized with the creation of the underlying `Payment` or `Refund` records. If any part of the operation fails, the entire transaction is rolled back, preventing orphaned records or misaligned balances. Additionally, the system employs Soft Deletes (via `SoftDeleteModel`) ensuring no financial entity is ever hard-deleted from the database, maintaining referential integrity for historical reporting.

## Audit Strategy
All financial transactions are immutable. The system does not allow direct updates to the amount or method of a `Payment` once it is recorded. Instead, corrections must be made through explicit, tracked operations like `FinancialAdjustment` or `Refund`. The overarching `AuditMiddleware` automatically logs the user, endpoint, and status of every request. Furthermore, sensitive operations (like refunds and credit adjustments) require explicit tracking of the `requested_by` and `approved_by` users, ensuring a clear chain of custody.

## Reconciliation Logic
Because SAMS is an offline-first financial system (handling primarily cash and external bank transfers), manual reconciliation is a core workflow. The `Payment` model includes a `reference_number` field to store external receipt numbers or bank transfer IDs. Operations staff use the dashboard to cross-reference these logged payments against actual bank statements or cash drawer counts. Approvals can be leveraged to mark bank transfers as "pending" until the funds actually clear in the academy's bank account, at which point an admin approves the payment, updating the invoice.

## Installment Logic
Installments are implemented via the `PaymentInstallment` model, which breaks down an `Invoice` into smaller, scheduled obligations. When a `Payment` is recorded against the master `Invoice`, the `FinancialService._update_installments()` method automatically cascades the paid amount to settle the earliest unpaid installments. This provides fine-grained tracking of what specific portion of a payment plan is overdue without losing the holistic view of the overall invoice balance.

## Reporting Optimization Strategy
To handle large datasets efficiently, the financial dashboards rely on database-level aggregation using Django's `Sum` and `Count` functions within `get_receivables_report`. This pushes the computational heavy lifting to PostgreSQL rather than processing lists in Python memory. For heavy exports, we use a Celery asynchronous task (`export_financial_report`) to generate CSVs and email them in the background, preventing API timeouts and blocking the main web server threads.
