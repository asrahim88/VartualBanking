
from django.urls import path
from . views import (
    UserRegistrationView, 
    CustomLoginView, 
    CustomLogOutView, 
    ProfileView, 
    UpdateUserInformationView, UpdateAddressInformationView, CustomPasswordChangeView, 
    
    # forgotten password for user 
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name= "register"),
    path("login/", CustomLoginView.as_view(), name= "login"),
    path("logout/", CustomLogOutView.as_view(), name= "logout"),
    path("profile/", ProfileView.as_view(), name= "profile"),
    path("updateUser/", UpdateUserInformationView.as_view(), name= "updateUser"),
    path("updateAddress/", UpdateAddressInformationView.as_view(), name= "updateAddress"),
    path("changePassword/", CustomPasswordChangeView.as_view(), name= "changePassword"),
    
    # forgotten password url
    path('password-reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
    path('password-reset/done/', 
         CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('reset/done/', 
         CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
] 

