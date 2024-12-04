from django.contrib import admin
from .models import UserBankingInformation, UserAddressInformation
from django.utils.html import format_html

class UserBankingInformationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'phone_number', 
        'birth_date', 
        'gender', 
        'account_type', 
        'account_number', 
        'balance',  
        'profile_image'
    )
    
    
    # Displaying profile image in the admin list view
    # def profile_image_tag(self, obj):
    #     if obj.profile_image:
    #         return format_html('<img src="{}" width="50" height="50" />'.format(obj.profile_image.url))
    #     return "No Image"
    # profile_image_tag.short_description = 'Profile Image'

    # Custom validation message on save
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class UserAddressInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'postal_code', 'country')

    # Custom validation message on save
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register the models
admin.site.register(UserBankingInformation, UserBankingInformationAdmin)
admin.site.register(UserAddressInformation, UserAddressInformationAdmin)
