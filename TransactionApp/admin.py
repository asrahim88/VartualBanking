from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','account', 'transaction_type', 'amount',"updated_balance", 'timestamp', 'is_approved')
    
    list_filter = ('transaction_type', 'is_approved')
    search_fields = ('account__user__username', 'transaction_type')
    
    ordering = ('-timestamp',)  # Latest transactions first
