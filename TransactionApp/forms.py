from django import forms
from .models import Transaction

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']  # Only amount

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']  # Only amount

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount



class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']  # Only amount

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Loan amount must be greater than zero.')
        return amount

# from django import forms
# from .models import Transaction, LoanRequest
# from .constants import TRANSACTION_TYPES


# class DepositForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['amount']


# class WithdrawForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['amount']


# class LoanRequestForm(forms.ModelForm):
#     class Meta:
#         model = LoanRequest
#         fields = ['amount_requested']
