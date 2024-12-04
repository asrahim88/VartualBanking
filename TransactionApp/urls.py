from django.urls import path
from .views import DepositView, WithdrawView, LoanRequestView, UserTransactionsView, AllLoanRequestView, LoanPaymentView


urlpatterns = [
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('loan-request/', LoanRequestView.as_view(), name='loan_request'),
    path('all_transaction_report/', UserTransactionsView.as_view(), name='all_transaction_report'),
    path('all_loan_request/', AllLoanRequestView.as_view(), name='all_loan_request'),
    path('loan-payment/<int:transaction_id>/', LoanPaymentView.as_view(), name='loan_payment'),
]

