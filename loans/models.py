from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('paid', 'Paid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # in MAD
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # percentage
    term_months = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    withdrawal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # in MAD
    
    def __str__(self):
        return f"Loan {self.id} - {self.user.username} - {self.amount} MAD"

class Repayment(models.Model):
    STATUS_CHOICES = [
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='due')
    
    def __str__(self):
        return f"Repayment for Loan {self.loan.id} - {self.amount} MAD"
