from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Transaction
from Accounts.models import UserBankingInformation
from .forms import DepositForm, WithdrawForm, LoanRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.views import View

class DepositView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = DepositForm
    template_name = 'deposit.html'
    success_url = reverse_lazy('all_transaction_report')

    login_url = "login" #for unauthenticated user redirect to login page

    def form_valid(self, form):
        # Current logged-in user
        user = self.request.user
        
        # Fetch UserBankingInformation for the user
        account = get_object_or_404(UserBankingInformation, user=user)

        # Set additional data in the form instance
        form.instance.account = account
        form.instance.transaction_type = 'deposit'  # Always deposit in this case
        

        # Update account balance
        account.balance += form.cleaned_data['amount']
        account.save()  # Save updated balance
        form.instance.updated_balance = account.balance

        return super().form_valid(form)


class WithdrawView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = WithdrawForm
    template_name = 'withdraw.html'
    success_url = reverse_lazy('all_transaction_report')

    login_url = "login" #for unauthenticated user redirect to login page
    
    def form_valid(self, form):
        # Current logged-in user
        user = self.request.user
        
        # Fetch UserBankingInformation for the user
        account = get_object_or_404(UserBankingInformation, user=user)

        # Check if sufficient balance exists
        if form.cleaned_data['amount'] > account.balance:
            form.add_error('amount', 'Insufficient balance.')
            return self.form_invalid(form)

        # Deduct amount from account balance
        account.balance -= form.cleaned_data['amount']
        account.save()

        # Set additional data for the transaction
        form.instance.account = account
        form.instance.transaction_type = 'withdraw'
        form.instance.updated_balance = account.balance
        return super().form_valid(form)
    


class LoanRequestView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = LoanRequestForm
    template_name = 'loan_request.html'
    success_url = reverse_lazy('loan_request')

    login_url = "login" # for unauthenticated user redirect to login page 
    
    def form_valid(self, form):
        # Current logged-in user
        user = self.request.user
        
        # Fetch UserBankingInformation for the user
        account = get_object_or_404(UserBankingInformation, user=user)

          # Check for unapproved loan requests
        unapproved_loans = Transaction.objects.filter(
            account=account, transaction_type='loan_request', is_approved=False
        ).count()

        if unapproved_loans >= 3:
            form.add_error('amount', 'You cannot request more than 3 loans until previous ones are approved.')
            return self.form_invalid(form)
        
        # Set additional data for the transaction
        form.instance.account = account
        form.instance.transaction_type = 'loan_request'

        # Loan requests are initially unapproved
        form.instance.is_approved = False
        
        
        return super().form_valid(form)

# <------------: All Transaction Report :-------------->

class UserTransactionsView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'user_transactions.html'
    context_object_name = 'transactions'
    # paginate_by = 5  # Pagination

    login_url = "login" # for unauthenticated user redirect to login page.
    
    def get_queryset(self):
        user = self.request.user
        account = user.Account  # Get the user's banking information

        # Get all transactions for the user
        transactions = Transaction.objects.filter(account=account)

        # Filter transactions by date range if provided
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            try:
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
                transactions = transactions.filter(timestamp__range=[start_date, end_date])
            except ValueError:
                transactions = []

        for transaction in transactions:
            transaction.account_number = account.account_number
            
        return transactions


#         unpaid  loan view
class AllLoanRequestView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'view_loan.html'  # আপনার টেমপ্লেটের নাম
    context_object_name = 'loan_requests' 
    
    login_url= "login" # for unauthenticated user redirect to login page
    
    def get_queryset(self):
        all_loan = Transaction.objects.filter(
            Q(transaction_type="loan_approval") | Q(transaction_type="loan_request")
        )
        return all_loan


# <--------------------: loan payment :---------------->

class LoanPaymentView(View):
    def post(self, request, transaction_id):
        # Get the transaction object where transaction_type is 'loan_request'
        transaction = get_object_or_404(Transaction, id=transaction_id, transaction_type="loan_approval")
        print(transaction)

        # Ensure the user has enough balance to pay
        account = transaction.account
        payment_amount = transaction.amount  # Full payment for the loan

        
        # Deduct the full loan amount from the user's balance
        account.balance -= payment_amount
        account.save()

        # Update the transaction
        # transaction.amount = 0  # Loan paid off
        transaction.transaction_type = "loan_paid"  # Mark as loan paid
        transaction.updated_balance = account.balance 
        transaction.save()
        return redirect('all_loan_request')
