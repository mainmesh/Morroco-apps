from rest_framework import serializers
from .models import Loan, Repayment

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = '__all__'