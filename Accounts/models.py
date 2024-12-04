from django.contrib.auth.models import User
from django.db import models
from . constants import ACCOUNT_TYPE, GENDER
from django.core.exceptions import ValidationError
import re


class UserBankingInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Account")
    phone_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)
    nid = models.CharField(max_length=10, unique=True)
    profile_image = models.ImageField(upload_to='accounts/profile_images/', blank=True, null=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
    
    # validation process
    def clean(self):
        
        # account
        account_number = self.account_number
        if len(account_number) < 12: 
            raise ValidationError('Account number must be at least 12 digits long.')
        if not account_number.isdigit():
            raise ValidationError('Account number must contain only numbers.')
        
        # balance and initial deposit
        if self.balance < 0:
            raise ValidationError('Balance cannot be negative.')
        
        
        
        # phone_number
        if not re.match(r'^\+?8801[3-9]\d{8}$', self.phone_number):  
            raise ValidationError({'phone_number': 'Invalid phone number format. It should be start with + and country code.'})

        # image
        if self.profile_image and not self.profile_image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError({'profile_image': 'Profile image must be a PNG, JPG, or JPEG file.'})
        

        # nid validation
        if len(self.nid) != 10:
            raise ValidationError({'nid': 'NID must be 10 characters long.'})
        if not self.nid.isdigit():
            raise ValidationError({'nid': 'NID must only contain numbers.'})
        
        return super().clean()
    
class UserAddressInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.city}, {self.country}"
    
    
    # validation process 
    def clean(self):
        postal_code = self.postal_code
        if len(postal_code) != 5 or not postal_code.isdigit():
            raise ValidationError('Postal code must be exactly 5 digits.')
        return super().clean()

