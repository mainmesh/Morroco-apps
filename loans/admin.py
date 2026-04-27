from django.contrib import admin
from .models import Loan, Repayment
from datetime import date, timedelta
from decimal import Decimal

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at', 'approved_at')
    list_filter = ('status', 'created_at')
    actions = ['approve_loans', 'reject_loans']

    def approve_loans(self, request, queryset):
        for loan in queryset:
            loan.status = 'approved'
            loan.approved_at = date.today()
            loan.save()
            # Generate repayments
            total_amount = loan.amount + (loan.amount * loan.interest_rate / 100)
            monthly_payment = total_amount / loan.term_months
            due_date = loan.approved_at
            for i in range(loan.term_months):
                due_date += timedelta(days=30)
                Repayment.objects.create(
                    loan=loan,
                    amount=monthly_payment,
                    due_date=due_date
                )
    approve_loans.short_description = "Approve selected loans"

    def reject_loans(self, request, queryset):
        queryset.update(status='rejected')
    reject_loans.short_description = "Reject selected loans"

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'due_date', 'status')
    list_filter = ('status', 'due_date')
