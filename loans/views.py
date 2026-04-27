from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Loan, Repayment, Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from .serializers import LoanSerializer, RepaymentSerializer
from decimal import Decimal

class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

class RepaymentViewSet(viewsets.ModelViewSet):
    serializer_class = RepaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Repayment.objects.filter(loan__user=self.request.user)

def home(request):
    loan_options = [
        {'amount': 500, 'fee': 50},
        {'amount': 1000, 'fee': 70},
        {'amount': 1500, 'fee': 100},
        {'amount': 2000, 'fee': 130},
        {'amount': 2500, 'fee': 160},
        {'amount': 3000, 'fee': 190},
        {'amount': 3500, 'fee': 220},
        {'amount': 3800, 'fee': 250},
        {'amount': 4500, 'fee': 280},
        {'amount': 5000, 'fee': 310},
        {'amount': 6000, 'fee': 370},
        {'amount': 7500, 'fee': 430},
        {'amount': 8000, 'fee': 490},
        {'amount': 10000, 'fee': 550},
        {'amount': 12000, 'fee': 610},
        {'amount': 15000, 'fee': 700},
    ]
    return render(request, 'loans/home.html', {'loan_options': loan_options})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'loans/register.html', {'form': form})

@login_required
def apply_loan(request, amount):
    if request.method == 'POST':
        # Process application
        loan = Loan.objects.create(
            user=request.user,
            amount=Decimal(amount),
            interest_rate=Decimal('10.00'),  # example
            term_months=12,  # example
            withdrawal_fee=Decimal(request.POST.get('fee', 0))
        )
        return redirect('dashboard')
    # Get fee for amount
    fees = {
        500: 50, 1000: 70, 1500: 100, 2000: 130, 2500: 160, 3000: 190,
        3500: 220, 3800: 250, 4500: 280, 5000: 310, 6000: 370, 7500: 430,
        8000: 490, 10000: 550, 12000: 610, 15000: 700
    }
    fee = fees.get(int(amount), 0)
    return render(request, 'loans/apply.html', {'amount': amount, 'fee': fee})

@login_required
def dashboard(request):
    loans = Loan.objects.filter(user=request.user)
    repayments = Repayment.objects.filter(loan__user=request.user)
    return render(request, 'loans/dashboard.html', {'loans': loans, 'repayments': repayments})

@login_required
def accounts(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            success_message = 'Your account information has been updated successfully.'
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=profile)
            return render(request, 'loans/accounts.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'success_message': success_message,
            })
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'loans/accounts.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    user_count = User.objects.count()
    loan_count = Loan.objects.count()
    repayment_count = Repayment.objects.count()
    total_deposited = Loan.objects.aggregate(total=Sum('withdrawal_fee'))['total'] or 0
    
    # New users over time (last 12 months)
    new_users_data = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('month')
    new_users_labels = [item['month'].strftime('%Y-%m') for item in new_users_data]
    new_users_counts = [item['count'] for item in new_users_data]
    
    # Deposits over time
    deposits_data = Loan.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('withdrawal_fee')).order_by('month')
    deposits_labels = [item['month'].strftime('%Y-%m') for item in deposits_data]
    deposits_totals = [float(item['total']) for item in deposits_data]
    
    # Loan statuses
    loan_statuses = Loan.objects.values('status').annotate(count=Count('id'))
    status_labels = [item['status'] for item in loan_statuses]
    status_counts = [item['count'] for item in loan_statuses]
    
    return render(request, 'loans/admin_dashboard.html', {
        'user_count': user_count,
        'loan_count': loan_count,
        'repayment_count': repayment_count,
        'total_deposited': total_deposited,
        'new_users_labels': new_users_labels,
        'new_users_counts': new_users_counts,
        'deposits_labels': deposits_labels,
        'deposits_totals': deposits_totals,
        'status_labels': status_labels,
        'status_counts': status_counts,
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'loans/admin_users.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def admin_loans(request):
    loans = Loan.objects.all()
    return render(request, 'loans/admin_loans.html', {'loans': loans})

@user_passes_test(lambda u: u.is_superuser)
def admin_repayments(request):
    repayments = Repayment.objects.all()
    return render(request, 'loans/admin_repayments.html', {'repayments': repayments})
