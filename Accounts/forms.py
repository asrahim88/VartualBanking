from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserBankingInformation, UserAddressInformation
from django.core.exceptions import ValidationError
from .constants import ACCOUNT_TYPE, GENDER
from django.contrib.auth.models import User
import re
from datetime import date
from django.contrib.auth.password_validation import validate_password
import random

# signup form / registration form

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER, required=True)
    nid = forms.CharField(max_length=20, required=True)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, required=True)
    street_address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=50, required=True)
    postal_code = forms.CharField(max_length=10, required=True)
    country = forms.CharField(max_length=50, required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'gender', 'nid', 'account_type', 'street_address', 'city', 'postal_code', 'country', 'profile_image', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_pattern = re.compile(r'^\+?8801[3-9]\d{8}$')
            if not phone_pattern.match(phone_number):
                raise ValidationError("Phone number must be start with '+8801' and 12 digits.")
            
        # Check if phone_number already exists
        if UserBankingInformation.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("This phone number is already registered.")
        return phone_number

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Profile image must be a PNG, JPG, or JPEG file.")
        return image

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if len(postal_code) != 5 or not postal_code.isdigit():
            raise ValidationError("Postal code must be exactly 5 digits.")
        return postal_code

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            if birth_date > date.today():
                raise ValidationError("Birth date cannot be in the future.")
            age = (date.today() - birth_date).days // 365
            if age < 18:
                raise ValidationError("You must be at least 18 years old.")
        return birth_date
    
    def clean_nid(self):
        nid = self.cleaned_data.get('nid')
        if len(nid) != 10:
            raise ValidationError('NID must be 10 characters long.')
        if not nid.isdigit():
            raise ValidationError('NID must only contain numbers.')
        # Check if nid already exists
        if UserBankingInformation.objects.filter(nid=nid).exists():
            raise ValidationError("This NID is already registered.")
        return nid

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        # Validate the password using Django's default password validators
        try:
            validate_password(password1, self.instance)
        except ValidationError as e:
            raise ValidationError(e)


        # Additional custom validations
        if len(password1) < 10:
            raise ValidationError("Password must be at least 10 characters long.")
        
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        if not re.search(r'\d', password1):
            raise ValidationError("Password must contain at least one digit.")
        
        if not re.search(r'[!@#$%^&*()_+=\-{};:"\',.<>?/\\|`~]', password1):
            raise ValidationError("Password must contain at least one special character.")
        return password2

    def generate_account_number(self):
        return str(random.randint(100000000000, 999999999999))

    def save(self, commit=True):
        # Save user instance
        our_user = super().save(commit=False)
        if commit:
            our_user.save()

        # Generate a unique account number
        account_number = self.generate_account_number()

        # Ensure the account number is unique in the database
        while UserBankingInformation.objects.filter(account_number=account_number).exists():
            account_number = self.generate_account_number()  # Generate a new one if the current one is not unique

        # Gather data for banking info
        account_type = self.cleaned_data.get('account_type')
        phone_number = self.cleaned_data.get('phone_number')
        birth_date = self.cleaned_data.get('birth_date')
        gender = self.cleaned_data.get('gender')
        nid = self.cleaned_data.get('nid')
        profile_image = self.cleaned_data.get('profile_image')
        street_address = self.cleaned_data.get('street_address')
        city = self.cleaned_data.get('city')
        postal_code = self.cleaned_data.get('postal_code')
        country = self.cleaned_data.get('country')

        banking_info = UserBankingInformation(
            user = our_user,
            account_type = account_type,
            account_number = account_number,
            phone_number = phone_number,
            birth_date = birth_date,
            gender = gender,
            nid = nid,
            profile_image = profile_image,
        )
        
        if commit:
            banking_info.save()

        # Save the address information
        address_info = UserAddressInformation(
            user=our_user,
            street_address=street_address,
            city=city,
            postal_code=postal_code,
            country=country
        )
        if commit:
            address_info.save()

        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                    ),
                    'placeholder': f'Enter your {field.replace("_", " ")}'
                }
            )


# <---------: Update User Information Form :----------->

class UpdateUserInformation(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER, required=True)
    nid = forms.CharField(max_length=20, required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'gender', 'nid','profile_image']

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set css class for all input fields from backend
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                    ),
                    'placeholder': f'Enter your {field.replace("_", " ")}'
                }
            )

        if self.instance:
            try:
                user_account = self.instance.Account
            except UserBankingInformation.DoesNotExist:
                user_account = None
                
            if user_account:
                self.fields["phone_number"].initial = user_account.phone_number
                self.fields["birth_date"].initial = user_account.birth_date
                self.fields["gender"].initial = user_account.gender
                self.fields["nid"].initial = user_account.nid
    
    def save(self, commit=True):
        our_user = super().save(commit=False)
        
        if commit:
            our_user.save()
            
            user_account, created  = UserBankingInformation.objects.get_or_create(user = our_user)
            
            user_account.phone_number = self.cleaned_data["phone_number"]
            user_account.birth_date = self.cleaned_data["birth_date"]
            user_account.gender = self.cleaned_data["gender"]
            user_account.nid = self.cleaned_data["nid"]
            user_account.save()
        return our_user



# <----------: Update Address Information Form :------->

class UpdateAddressInformationForm(forms.ModelForm):
    street_address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=50, required=True)
    postal_code = forms.CharField(max_length=10, required=True)
    country = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ["street_address", "city", "postal_code", "country"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                    ),
                    'placeholder': f'Enter your {field.replace("_", " ")}'
                }
            )
        if self.instance:
            try:
                user_address = self.instance.address
            except UserAddressInformation.DoesNotExist:
                user_address = None
                
            if user_address:
                self.fields["street_address"].initial = user_address.street_address
                self.fields["city"].initial = user_address.city
                self.fields["postal_code"].initial = user_address.postal_code
                self.fields["country"].initial = user_address.country
                
                
    def save(self, commit=True):
        our_user = super().save(commit=False)
        
        if commit:
            our_user.save()
            
            user_account, created  = UserAddressInformation.objects.get_or_create(user = our_user)
            
            user_account.street_address = self.cleaned_data["street_address"]
            user_account.city = self.cleaned_data["city"]
            user_account.postal_code = self.cleaned_data["postal_code"]
            user_account.country = self.cleaned_data["country"]
            user_account.save()
        return our_user