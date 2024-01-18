from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect
from django.contrib import messages

def admin_login():
    def decorator(func):
        def wrap(request,*args,**kwargs):
            if request.user.is_staff == 1:
                return func(request,*args,**kwargs)
            else:
                messages.warning(request,'Invalid Credentials')
                return redirect('loginpage')
        return wrap
    return decorator

def user_login():
    def decorator(func):
        def wrap(request,*args,**kwargs):
            if request.user.is_staff == 0: 
                return func(request,*args,**kwargs)
            else:
                messages.warning(request,'Invalid Credentials')
                return redirect('userLoginpage')
        return wrap
    return decorator