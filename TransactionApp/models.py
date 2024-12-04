from django.db import models
from Accounts.models import UserBankingInformation
from django.core.exceptions import ValidationError
from . constants import TRANSACTION_TYPES


# Transaction Model

class Transaction(models.Model):
    account = models.ForeignKey(UserBankingInformation, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # For loan requests
    updated_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Updated balance field

    def __str__(self):
        return f"{self.account.user.username} - {self.transaction_type} - {self.amount} {self.id}"

    def save(self, *args, **kwargs):
        
        if self.transaction_type == 'loan_request' and self.is_approved:
            # Update account balance
            if not self.account.balance:
                self.account.balance = 0  # Ensure balance is not None
            self.account.balance += self.amount
            self.account.save()
            self.updated_balance = self.account.balance
            self.transaction_type = "loan_approval"
        super().save(*args, **kwargs)
