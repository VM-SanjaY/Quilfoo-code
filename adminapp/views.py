from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import *
from .forms import *
from loginapp.models import Websiteuser, Temperorytable
from quilfooapp.models import *
from django.db.models import Count
from django.core import serializers
from django.http import HttpResponse

# Create your views here.

# ----------------------------- Admin login ------------------------------------------------
def adminlogin(request):
    if request.user.is_superuser:
        return redirect('adminhome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if '@' in username:
                try:
                    usermodal = User.objects.filter(username=username)     
                except:
                    usermodal = User.objects.filter(email=username)
                if usermodal.exists():
                    user = authenticate(username=usermodal[0].username, password=password)
                else:
                    user = None
            else:
                user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('adminhome')
                else:
                    return redirect('/')
            else:
                messages.info(request, "Username or Password is incorrect")
        return render(request, 'logs/loginpage.html')
    

def adminlogout(request):
    logout(request)
    return redirect('/admin/')

# ------------------------------------- Dashboard page -------------------------------------------


def adminhome(request):
    if request.user.is_superuser or request.user.is_staff:
        page = "Dashboard"
        userc = Websiteuser.objects.all().exclude(webuser=request.user)
        usercount = userc.count()
        post = UserPost.objects.all()
        postcount = post.count()
        question = UserQuestion.objects.all()
        questioncount = question.count()
        answer = AnswerQuestion.objects.all()
        answercount = answer.count()
        context = {"page":page,"usercount":usercount,"postcount":postcount,"questioncount":questioncount,"answercount":answercount}
        return render(request,'pages/dashboard/dashboard.html',context)
    else:
        return redirect ('userpage')

# -------------------------------------  Profile table-------------------------------------------------

def adminprofile(request,pk):
    if request.user.is_superuser:
        page = "Profile"
        profiledetail = Websiteuser.objects.get(webuser=pk)
        context = {"page":page,"profiledetail":profiledetail}
        return render (request, 'pages/profile/adminprofile.html',context)
    else:
        return redirect('/')
    

def editadminprofile(request,pk):
    if not request.user.is_superuser:
        return redirect('/')

    page = "Profile"
    profiledetail = Websiteuser.objects.get(pk=pk)
    form = WebsiteuserForm()
    form = WebsiteuserForm(instance=profiledetail)
    if request.method == "POST":
        form = WebsiteuserForm(request.POST,request.FILES , instance=profiledetail)             
        if form.is_valid(): 
            project = form.save(commit = False)
            project.save()
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        linkedin = request.POST.get('linkedin')
        quora = request.POST.get('quora')
        reddit = request.POST.get('reddit')
        facebook = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        instagram = request.POST.get('instagram')
        profilepic = request.FILES.get('profilepic')
        coverpic = request.FILES.get('coverpic')
        shortbio = request.POST.get('shortbio')
        print(profilepic,coverpic)
        if location.isdigit():
            messages.error(request, 'Location should not have numbers')
            return redirect('editadminprofile')

        if not phone.isdigit():
            messages.error(request, 'Please provide a valid phone number')
            return redirect('editadminprofile')

        # Update User model
        user = User.objects.get(username=request.user.username)
        user.first_name = name
        user.username = username
        user.email = email
        user.save()

        # Update Websiteuser model
        profiledetail.webuser = user
        profiledetail.phonefield = phone
        profiledetail.location = location
        profiledetail.linkedin = linkedin
        profiledetail.quora = quora
        profiledetail.reddit = reddit
        profiledetail.facebook = facebook
        profiledetail.twitter = twitter
        profiledetail.instagram = instagram
        if profilepic:
            profiledetail.profilepic = profilepic
        if coverpic:    
            profiledetail.coverpic = coverpic
        profiledetail.shortbio = shortbio
        profiledetail.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('adminprofile', pk=request.user.id )


    context = {"page": page, "profiledetail": profiledetail,"form":form}
    return render(request, 'pages/profile/editprofile.html', context)


def changePasswordAdmin(request,pk):
    if not request.user.is_superuser:
        return redirect('/')
    admindetail = Websiteuser.objects.get(pk=pk)
    page = "Profile"
    data ={}
    if request.method == "POST":
        currentpassword =  request.POST.get('currentpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        if currentpassword:
            user = User.objects.get(username=request.user.username)
            if check_password(currentpassword, user.password):
                if newpassword == confirmpassword:
                    hashed_password = make_password(newpassword)
                    user.password = hashed_password
                    user.save()
                else:
                    data['password'] ="New password does not match with Confirm Password"
            else:
                data['curpassword'] = 'Please enter your correct current password'
                

    context = {"page":page,"admindetail":admindetail,"data":data}
    return render(request,'pages/profile/changepassword.html',context)


# ---------------------------------- Usertable --------------------------------------

def adminusertable(request):
    if request.user.is_superuser:
        page = "User-Table"
        customerdetail = Websiteuser.objects.all().exclude(webuser=request.user)
        context = {"page":page,"customerdetail":customerdetail}
        return render(request,'pages/tables/usertable.html',context)
    else:
        return redirect ('userpage')
    

def editadminusertable(request,pk):
    if request.user.is_superuser:
        page = "User-Table"
        editprofile = Websiteuser.objects.get(id=pk)
        form = WebsiteuserForm()
        form = WebsiteuserForm(instance=editprofile)
        if request.method == "POST":
            form = WebsiteuserForm(request.POST,request.FILES , instance=editprofile)             
            if form.is_valid(): 
                project = form.save(commit = False)
                project.save()
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            location = request.POST.get('location')
            linkedin = request.POST.get('linkedin')
            quora = request.POST.get('quora')
            reddit = request.POST.get('reddit')
            facebook = request.POST.get('facebook')
            twitter = request.POST.get('twitter')
            instagram = request.POST.get('instagram')
            profilepic = request.FILES.get('profilepic')
            coverpic = request.FILES.get('coverpic')
            shortbio = request.POST.get('shortbio')
            print(profilepic,coverpic)
            if location.isdigit():
                messages.error(request, 'Location should not have numbers')
                return redirect('editadminprofile')

            if not phone.isdigit():
                messages.error(request, 'Please provide a valid phone number')
                return redirect('editadminprofile')

            # Update User model
            user = User.objects.get(username=editprofile.webuser.username)
            user.first_name = name
            user.username = username
            user.email = email
            user.save()

            # Update Websiteuser model
            editprofile.webuser = user
            editprofile.phonefield = phone
            editprofile.location = location
            editprofile.linkedin = linkedin
            editprofile.quora = quora
            editprofile.reddit = reddit
            editprofile.facebook = facebook
            editprofile.twitter = twitter
            editprofile.instagram = instagram
            if profilepic:
                editprofile.profilepic = profilepic
            if coverpic:    
                editprofile.coverpic = coverpic
            editprofile.shortbio = shortbio
            editprofile.save()
            messages.success(request, 'User - Profile updated successfully')
            return redirect('adminusertable')

        context = {"page":page,"editprofile":editprofile,"form":form}
        return render(request,'pages/tables/editusertable.html',context)
    else:
        return redirect ('userpage')


# ----------------------------------- Temporary table page  ------------------------------------------

def admintemporarytable(request):
    if request.user.is_superuser:
        page = "Temporary Table"
        customerdetail = Temperorytable.objects.all()
        context = {"page":page,"customerdetail":customerdetail}
        return render(request,'pages/tables/temptable.html',context)
    else:
        return redirect ('userpage')
    

def editadmintemporarytable(request,pk):
    if request.user.is_superuser:
        page = "Temporary Table"
        edittempuser = Temperorytable.objects.get(id=pk)
        if request.method == "POST":
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            otp = request.POST.get('otp')
            
            if name:
                edittempuser.name = name
                edittempuser.username = username
                edittempuser.email = email
                edittempuser.phonefield = phone
                edittempuser.password = password
                edittempuser.otp = otp
                edittempuser.save()
                return redirect ('admintemporarytable')

        context = {"page":page,"edittempuser":edittempuser}
        return render(request,'pages/tables/edittemporarytable.html',context)
    else:
        return redirect ('userpage')

# ------------------------------------- Report index ---------------------------------------------------
# def reportPost(request):
#     report_datas=[]
#     report_data = Reportpost.objects.values('reportedon_id').annotate(reportedon_id_count=Count('reportedon_id')).order_by('-reportedon_id_count').filter(reportedon_id_count__gt=1)
#     data= [ sub['reportedon_id'] for sub in report_data ]
#     for postid in data:
#         datas = Reportpost.objects.filter(reportedon_id=postid).first()
#         report_datas.append(datas)
#     return render(request,'pages/reports/reportIndex.html',{'report_datas':report_datas})

def reportPost(request):
    if request.user.is_superuser:
        page = "Report on Post"
        reports = UserPost.objects.filter(report_count__gte=5).order_by('-report_count')
        context ={"reports":reports,"page":page}
        return render(request,'pages/reports/reportIndex.html',context)

# ------------------------------------ Report User Detail -------------------------------------------
# def reportPostUser(request,pk):
#     reporters = Reportpost.objects.filter(reportedon_id=pk)
#     post_details = Reportpost.objects.filter(reportedon_id=pk).first()
#     print(post_details)
#     context = {
#         'reporters':reporters,
#         'post_details':post_details
#     }
#     return render(request,'pages/reports/reportPostUser.html',context)


def reportPostUser(request,pk):
     if request.user.is_superuser:
        page = "Report on Post"
        report = UserPost.objects.get(pk=pk)
        try:
            details = Reportpost.objects.filter(reported_on=pk)
        except:
            details = None       
        context = {"details":details,"page":page,"report":report}
        return render(request,'pages/reports/reportPostUser.html',context)


def reportAnswer(request):
    if request.user.is_superuser:
        page = "Report on Answer"
        reports = AnswerQuestion.objects.filter(report_count__gte=5).order_by('-report_count')
        context={"reports":reports,"page":page}
        return render(request,'pages/reports/reportanswer.html',context)

def reportAnsweruser(request,pk):
    if request.user.is_superuser:
        page = "Report on Answer"
        report = AnswerQuestion.objects.get(pk=pk)
        details = ReportOnAnswer.objects.filter(reported_on=pk)
        context = {"details":details,"page":page,"report":report}
        return render(request,'pages/reports/reportAnswerUser.html',context)


# --------------------------------   Category page -------------------------------------------------
def category(request):
    if request.user.is_superuser:
        page = "Category Table"
        categorylist = Category.objects.all()
        context = {"page":page,"categorylist":categorylist}
        return render(request,'pages/category/category.html',context)
    else:
        return redirect ('userpage')

def addCategory(request):
    if request.user.is_superuser:
        page = "Category Table"
        if request.method == "POST":
            topic = request.POST.get('name')
            topicimage = request.FILES.get('topicimage')
            if topicimage:
                data = Category(
                    topic=topic,
                    image=topicimage,
                )
                data.save()
                return redirect('category')
        context = {"page":page}
        return render(request,'pages/category/addcategory.html',context)
    else:
        return redirect ('userpage')


def editCategory(request,pk):
    if request.user.is_superuser:
        page = "Category Table"
        categorydata = Category.objects.get(id=pk)
        if request.method == "POST":
            name = request.POST.get("name")
            image = request.FILES.get('topicimage')
            deleteadata = request.POST.get('deletedata')
            if deleteadata:
                deleteadata = deleteadata.lower()
                if deleteadata == "yes":
                    Category.objects.get(id=pk).delete()
                    return redirect('category')
            if name:
                categorydata.topic = name
                if image:
                    categorydata.image = image
                categorydata.save()
                return redirect('category')

        
        context = {"page":page,"categorydata":categorydata}
        return render(request,'pages/category/editcategory.html',context)
    else:
        return redirect ('userpage')
    
# ------------------------------------- Map page -------------------------------------------

def userLocateMap(request):
    if request.user.is_superuser:
        page = "Map"
        context = {"page":page}
        return render(request,'pages/map/maps.html',context)
    else:
        return redirect ('userpage')
    

# ------------------------------------- Notification page --------------------------------------


def adminNotification(request):
    if request.user.is_superuser:
        page = "Notification"
        aduser = Websiteuser.objects.filter(webuser=request.user)
        aduser = aduser[0]
        notify = aduser.messages.all().order_by('status')
        unreadcount = notify.filter(status=False).count()
        context ={"page":page,"notify":notify,"unreadcount":unreadcount}
        return render(request,'pages/notification/notification.html',context)
    else:
        return redirect ('userpage')


def adminMessageOfNoti(request,pk):
    if request.user.is_superuser:
        page = "Notification"
        aduser = Websiteuser.objects.filter(webuser=request.user)
        aduser = aduser[0]
        messageget = aduser.messages.get(id=pk)
        if messageget.is_read == False:
            messageget.is_read = True
            messageget.save()
        if request.method == "POST":
            if "mark_unread" in request.POST:
                messageget.is_read = False
                messageget.save()
                return redirect('adminNotification')
        context = {"messageget": messageget,"page":page}

        return render(request,'pages/notification/messagenotify.html',context)
    else:
        return redirect ('userpage')

# ----------------------------------- Agreement Page ------------------------------------------

def agreementpage(request):
    if request.user.is_superuser:
        page = "Terms and Conditions"
        aduser = Websiteuser.objects.filter(webuser=request.user)
        aduser = aduser[0]
        agreementinfo = AgreementData.objects.get(creaby=aduser)
        context = {"agreementinfo": agreementinfo, "page": page}
        return render(request, 'pages/agreement/agreementpage.html', context)
    else:
        return redirect('userpage')



def editAgreementpage(request):
    if request.user.is_superuser:
        pages = "Terms and Conditions"
        aduser = Websiteuser.objects.filter(webuser=request.user)
        aduser = aduser[0]
        agreementinfo = AgreementData.objects.get(creaby=aduser)
        form = AgreementdetailForm()
        form = AgreementdetailForm(instance=agreementinfo)
        if request.method == "POST":
            form = WebsiteuserForm(request.POST,request.FILES , instance=agreementinfo)             
            dep = request.POST.get('description')
            if dep:
                agreementinfo.description = dep
                agreementinfo.save()
                return redirect('agreementpage')

        context = {"form":form,"pages":pages}
        return render(request,'pages/agreement/editagreement.html',context)
    else:
        return redirect ('userpage')