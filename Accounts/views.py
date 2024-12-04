from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView 
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm, UpdateUserInformation, UpdateAddressInformationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import UserAddressInformation, UserBankingInformation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


# <-----------------: Profile View :------------------->

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # User information
        context['user'] = user
        
        # Banking information
        try:
            context['banking_info'] = UserBankingInformation.objects.get(user=user)
        except UserBankingInformation.DoesNotExist:
            context['banking_info'] = None

        # Address information
        try:
            context['address_info'] = UserAddressInformation.objects.get(user=user)
        except UserAddressInformation.DoesNotExist:
            context['address_info'] = None

        return context


# <-----------: Update user information :-------------->

@method_decorator(login_required, name='dispatch')
class UpdateUserInformationView(UpdateView):
    model = User
    form_class = UpdateUserInformation
    template_name = 'updateUser.html'
    
    def get_object(self, queryset=None):
        return self.request.user  # Get the currently logged-in user
    
    def form_valid(self, form):
        # Save the form but do not commit yet
        user = form.save(commit=False)
        user.save()  # Save the User model
        
        # Now update the UserBankingInformation model fields
        user_account, created = UserBankingInformation.objects.get_or_create(user=user)
        user_account.phone_number = form.cleaned_data['phone_number']
        user_account.birth_date = form.cleaned_data['birth_date']
        user_account.gender = form.cleaned_data['gender']
        user_account.nid = form.cleaned_data['nid']
        
        # Handle profile image update
        if form.cleaned_data.get('profile_image'):
            user_account.profile_image = form.cleaned_data['profile_image']
        
        try:
            user_account.save()  
        except IntegrityError:
            # Handle IntegrityError when phone number is not unique
            form.add_error('phone_number', 'This phone number is already in use. Please use a different one.')
            return render(self.request, 'updateUser.html', {'form': form, 'error': 'This phone number is already in use.'})
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


# <--------------:Update User Address :---------------->

@method_decorator(login_required, name='dispatch')
class UpdateAddressInformationView(UpdateView):
    model = User
    form_class = UpdateAddressInformationForm
    template_name = 'updateAddress.html'
    
    
    def get_object(self, queryset=None):
        return self.request.user  # This will get the currently logged-in user
    
    def form_valid(self, form):
        
        user = form.save(commit=False)
        user.save()  # Save the User model
        
        # Now update the UserAddressInformation model fields
        user_address, created = UserAddressInformation.objects.get_or_create(user=user)
        user_address.street_address = form.cleaned_data['street_address']
        user_address.city = form.cleaned_data['city']
        user_address.postal_code = form.cleaned_data['postal_code']
        user_address.country = form.cleaned_data['country']
        
        user_address.save()  
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


# <------------------: Registration :------------------>

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  
            return redirect('profile') 
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        
        # if form valid after show that
        return self.render_to_response(self.get_context_data(form=form))


# <-------------------: Login View :------------------->

class CustomLoginView(LoginView):
    template_name = 'login.html' 
    redirect_authenticated_user = True  
    next_page = reverse_lazy('profile')  
    
# <------------------: Logout View :------------------>
 
class CustomLogOutView(LogoutView):
    next_page = reverse_lazy("login")
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# <---------: password change for login user :--------->

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile') 
    success_message = "Your password has been successfully updated."


#<--------: password change for forgotten user :------->

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgotten_password/password_reset.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home') 
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'forgotten_password/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'forgotten_password/password_reset_confirm.html'
    
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'forgotten_password/password_reset_complete.html'


