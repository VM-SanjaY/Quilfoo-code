from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from loginapp.models import *
from random import randint
from Quilfoo import settings
from django.core.mail import EmailMessage
import re
from  Quilfoo.decorators import *
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
# Create your views here.

#------------------- User login ---------------------------
def loginpage(request):
    login_errors={}
    old_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username =="":
            login_errors['username'] = 'Please Enter Username or Email'
        if password =="":
            login_errors['password'] = 'Please Enter Password'
        old_data={'username':username}
        if username !='' and '@' in username:
            check_username = User.objects.filter(username=username).first()
            check_email = User.objects.filter(email=username).first()
            if check_username:
                username=check_username
            if check_email:
                username=check_email
        
        if login_errors =={}:
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('userCategory')
            else:
                messages.warning(request,'Invalid Credentials')
            
    context={'login_errors':login_errors,'old_data':old_data}
    return render(request,'loginpage.html',context)

#--------------------------------- User Registertion ------------------------------- -----------------
def registerpage(request):
    registor_errors = {}
    old_data = {}
    if request.method == 'POST':
        global usernameofuser
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        terms = request.POST.get('terms')
        
        #---------------- Validations---------------------
        if name =="":
            registor_errors['name'] = 'Please, enter your name!'
            
        if username =="":
            registor_errors['username'] = 'Please enter a username.'
        #-----------Username unique validation--------------------
        elif username != "":
            username_valid = User.objects.filter(username=username)
            if username_valid:
                registor_errors['username'] = 'This Username is already taken'
                  
        if email =="":
            registor_errors['email'] = 'Please Enter the Email'
        #------------- Email Format validation ----------------------
        elif email!="":
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if(re.fullmatch(regex, email)):
                email_valid = User.objects.filter(email=email)
                if email_valid:
                    registor_errors['email'] = 'This Email is already taken'
            else:
                registor_errors['email'] = 'Please enter a valid Email adddress!'
                
        if password =="":
            registor_errors['password'] = 'Please enter your password!'
        if confirmpassword =="":
            registor_errors['confirmpassword'] = 'Please enter your confirm password!'
        if password !='' and confirmpassword !='':
            if password != confirmpassword:
                registor_errors['password'] = 'Password miss match'

        if terms ==None:
            registor_errors['terms'] = 'Please Agree the terms and conditions'
        #----------------------- Old data --------------------------------
        old_data = {'name':name,'username':username,'email':email}
        #---------------------- Send Email --------------------------------
        if registor_errors == {}:
            otp = randint(1111,9999)
            print('otp',otp,email)
            html_message = "Your one time password -"+" "+ str(otp)+"\n \n Use this OTP to register"
            subject = "OTP request"
            email_from = settings.EMAIL_HOST_USER
            email_to = [email]
            message = EmailMessage(subject,html_message,email_from,email_to)
            message.send()
            messages.success(request,"one time password sent to your mail")
            #----------- check and delete old session ---------------------
            if username in request.session:
                print('fsfgs', request.session[username])
                del request.session[username]
            if 'otp'in request.session:
                del request.session['otp']
            request.session[username] = [str(otp),name,username,email,password]
              
            #---------------------- Creating Session --------------------------
            request.session['email'] = email
            request.session['resendOtp'] = username
            return redirect('userOtppage',username=username)       
        
    context = {'registor_errors':registor_errors,'old_data':old_data}
    return render(request,'registerpage.html',context)


#------------------- User Registertion OTP ---------------------------
def otppage(request,username):
    if 'email' not in request.session:
        return redirect('userRegisterpage')
    errors = {}
    if request.method == "POST":
        one = request.POST.get('one')
        two = request.POST.get('two')
        three = request.POST.get('three')
        four = request.POST.get('four')
        
        #--------------- Validations-----------------------
        if one!='' and two!='' and three!='' and four!='': 
            #-------- Check Session is Empty or Not ----------
            if username in request.session:
                
                #--------------- Get Session Value----------------
                if 'otp' in request.session:
                    old_otp =str(request.session['otp'])
                else:
                    otp_user = request.session[username]
                    old_otp = str(otp_user[0])
                    
                user_datas = request.session[username]
                user_otp = (str(one)+str(two)+str(three)+str(four))
                print(old_otp,user_otp)
                if user_otp == old_otp:
                    #------------------ Data Insert User Table----------------
                    register_data = User.objects.create_user(first_name = user_datas[1],username = user_datas[2],email = user_datas[3],password = user_datas[4],is_superuser = 0)
                    register_data.save()
                    
                    #------------------ Data Insert WebsiteUser Table ----------------
                    user_id = User.objects.filter(username = username).first()
                    user_data = Websiteuser(webuser_id=user_id.id)
                    user_data.save()
                    #-------- Session destroy -------
                    del request.session[username]
                    del request.session['email']
                    del request.session['resendOtp']
                    if 'otp' in request.session:
                        del request.session['otp']
                    messages.success(request,'Registration Success')
                    return redirect('userLoginpage')
                else:
                    messages.warning(request,'OTP miss match')
        else:
            errors['otp'] = 'Please enter all fields'
    return render(request,'otppage.html',{'errors':errors})

#------------------- Resend OTP ---------------------------
def resendOtp(request):
    if 'resendOtp' not in request.session:
        return redirect('userRegisterpage')
    username = request.session['resendOtp']
    user_otp = request.session[username]
    otp = randint(1111,9999)
    request.session['otp']=otp
    html_message = "Your one time password -"+" "+ str(otp)+"\n \n Use this OTP to register"
    subject = "OTP request"
    email_from = settings.EMAIL_HOST_USER
    email_to = [user_otp[3]]
    message = EmailMessage(subject,html_message,email_from,email_to)
    message.send()
    messages.success(request,"one time password resend to your mail")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#-------------------------------------- Forgot Password ----------------------------------
def forgotpassword(request):
    error={}
    if request.method=='POST':
        email = request.POST.get('email')
        if email:
            user_email = User.objects.filter(email=email)
            if user_email:
                user_email = User.objects.get(email=email)
                html_message = render_to_string(
                'email.html',
                {'id': user_email.id})
                subject = "Forgot Password Request"
                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                message = EmailMultiAlternatives(subject,html_message,email_from,email_to)
                message.attach_alternative(html_message, "text/html")
                message.send()
                messages.success(request,"Please Check your mail")
            else:
                error={'email':'Please enter a valid Email adddress!'}
        else:
            error={'email':'Please enter the email'}

    return render(request,'forgotpassword.html',{'error':error})

#----------------------------------- User logout -----------------------------------------
def changepassword(request,id):
    errors ={}
    if request.method=="POST":
        pws = request.POST.get('password')
        c_pws = request.POST.get('confirm_password')
        if len(pws) > 6:
            if pws ==c_pws:
                data = User.objects.filter(id=id)
                data.update(password=make_password(pws))
                messages.success(request,"Your password has been changed ")
                return redirect('userLoginpage')
        else:
            errors['length']='please enter atleast 8 character'
    context={'errors':errors}
    return render(request,'setnewpassword.html',context)

#----------------------------------- User logout -----------------------------------------
@user_login()
def logoutpage(request):
    logout(request)
    return redirect('userLoginpage')    