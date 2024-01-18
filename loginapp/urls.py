from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user-login/',views.loginpage,name="userLoginpage"),
    path('sign-up/',views.registerpage,name="userRegisterpage"),
    path('sign-up/otp/str<username>',views.otppage,name="userOtppage"),
    path('user-logout/',views.logoutpage,name="userLogoutpage"),
    path('resend-otp/',views.resendOtp,name="resendOtp"),
    path('forgot-password-email/',views.forgotpassword,name="forgotpassword"),
    path('forgot-password/<id>/',views.changepassword,name="changepassword"),
]
