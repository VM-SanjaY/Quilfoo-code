from django.shortcuts import render,redirect
from .models import *
from postapp.models import *
from django.contrib.auth.models import User
from loginapp.models import *
from django.db.models import Q
from Quilfoo.decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.core import serializers
from .forms import WebsiteuserForm
from django.db.models import Count
import operator
from django.contrib import messages


# Create your views here.
def userdetails(request):
    if request.user.is_authenticated:
        print('hi',request.user)
        datas=Websiteuser.objects.get(webuser_id=request.user)
        return datas
        

#-------------------------------- User Category -----------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def category(request):
    user_data = Websiteuser.objects.get(webuser=request.user.id)
    if CategoryFollower.objects.filter(webuserid_id=user_data.id):
        return redirect('userHome')
    category = Category.objects.all()
    category_errors={}
    if request.method=='POST':
        if (len(request.POST)-1) >=5:
            if category_errors=={}:
                count=0
                for id in request.POST:
                    print('fwsfsf',id)
                    if count!=0:
                        data = CategoryFollower(categoryid_id=id,webuserid_id=user_data.id).save() 
    
                    count=1            
                return redirect('userHome')
        else:
            category_errors['category']="Select atleast 5 Topics"
    context = {'categorys':category,'category_errors':category_errors}
    return render(request,'userCategory.html',context)

#---------------------------------- Follow Unfollow Page -------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def followUnfollow(request):
    following=0
    follow=""
    follow_id = request.GET['post_id']
    user_id = Websiteuser.objects.get(webuser_id=request.user.id)
    datas = Follower.objects.filter(following_id=follow_id,webuserid_id=user_id.id)
    if datas:
        follow_data = Follower.objects.get(following_id=follow_id,webuserid_id=user_id.id)
        print(follow_data.following_id)
        if follow_data.following_id !=0:
            datas.delete()
            # print('jjj',follow_id)
            # following=0
            follow = 'Follow'
        else:
            following=follow_id
            follow = 'Following'
            data = datas.update(following_id=following,webuserid_id=user_id.id)
    else:
        follow = 'Following'
        following=follow_id
        data = Follower(following_id=following,webuserid_id=user_id.id)
        data.save()
    print(follow_id,follow)
    return JsonResponse({"id" : follow_id,
                        "follow" : follow}, status=200)

#---------------------------------- User Home Page -------------------------------------------------
def home(request):
    user_details = userdetails(request)
    datas =[]
    follow = []
        
    if request.path =='/quilfoo/':
        #-------------------- Follow User Home Page -------------------------------
        if request.user.is_authenticated:
            print('if')
            user_id = Websiteuser.objects.get(webuser_id = request.user.id)
            follower = Follower.objects.filter(webuserid_id=user_id.id)
            for i in follower:
                follow.append(i.following_id)
                
            user_posts = UserPost.objects.all().order_by('-id').prefetch_related("children")
            
            #-------------------- Get Following id -----------------------------
            post_id=[]
            post_datas=[]
            for j in follow:
                user_post = UserPost.objects.filter(postby_id=j).order_by('-id')
                for k in user_post:
                    # user_post = UserPost.objects.get(id=k.id)
                    post_id.append(k.id)
            post_id.sort(reverse=True)
            for post_data in post_id:
                user_post = UserPost.objects.get(id=post_data)
                post_datas.append(user_post)
                
            #------------------- User recent Post  ---------------------------
            if post_id !=[]:
                user_data = UserPost.objects.filter(postby_id=user_id.id,id__gt=post_id[0]).order_by('-created_at')
                print('hello',post_id[0],user_data)
                for p in user_data:
                    parent_data = {}
                    parent_data['user_post'] = UserPost.objects.get(id=p.id)
                    parent_data["upvote"] = p.children.filter(userpostid_id = p.pk,Upvote = 1).count()
                    parent_data["downvote"] = p.children.filter(userpostid_id = p.pk,downvote = 1).count()
                    datas.append(parent_data)
            #------------------- Following Post---------------------------
            for p in post_datas:
                parent_data = {}
                parent_data['user_post'] = UserPost.objects.get(id=p.id)
                parent_data["upvote"] = p.children.filter(userpostid_id = p.pk,Upvote = 1).count()
                parent_data["downvote"] = p.children.filter(userpostid_id = p.pk,downvote = 1).count()
                datas.append(parent_data)
                
            #------------------- All Post Except Following---------------------------
            for p in user_posts:
                parent_data = {}
                parent_data['user_post'] = UserPost.objects.get(id=p.id)
                parent_data["upvote"] = p.children.filter(userpostid_id = p.pk,Upvote = 1).count()
                parent_data["downvote"] = p.children.filter(userpostid_id = p.pk,downvote = 1).count()
                if parent_data['user_post'].postby_id  not in follow:
                    print(parent_data['user_post'].postby_id)
                    datas.append(parent_data)
        else:
            return redirect('beforeLogin')
    
    else:
        if request.path =='/':
            if request.user.is_authenticated:
                return redirect('userHome')
            data = UserPostUpvoteDownvote.objects.all()
            ids =[]
            for id in data:
                ids.append(id.userpostid_id)
            id_list = list(set(ids))
            
            post_data_count ={}
            for count in id_list:
                counts = UserPostUpvoteDownvote.objects.values('id').filter(userpostid_id=count).count()
                post_data_count[count]=counts
            sort_data = dict(sorted(post_data_count.items(),key=operator.itemgetter(1),reverse=True))
            print('data',sort_data)
            temp_data=[]
            for id in  sort_data:
                user_posts = UserPost.objects.get(id=id)
                temp_data.append(user_posts)
                
            for p in temp_data:
                parent_data = {}
                parent_data['user_post'] = UserPost.objects.get(id=p.id)
                parent_data["upvote"] = p.children.filter(userpostid_id = p.pk,Upvote = 1).count()
                parent_data["downvote"] = p.children.filter(userpostid_id = p.pk,downvote = 1).count()
                datas.append(parent_data)
    #------------------------------ Category -----------------------------------
    categorys_list = Category.objects.all()
    category={}
    if request.user.is_authenticated:
        user = Websiteuser.objects.get(webuser_id = request.user.id)
        categorys_follower = CategoryFollower.objects.filter(webuserid_id=user.id)
        categorys_follower_data= []
        for i in categorys_follower:
            categorys_follower_data.append(i.categoryid_id)
            
        temp={}
        for i in categorys_list:
            count = CategoryFollower.objects.filter(categoryid_id=i.id).count()
            temp[i.id]=count
        sort_data = dict(sorted(temp.items(),key=operator.itemgetter(1),reverse=True))
        
        categorys=[]
        for j in sort_data:
            if j not in categorys_follower_data:
                categorys.append(Category.objects.get(id=j))  
        category['category'] = categorys
        category['categorys_follower'] = categorys_follower
    else:
        category['category'] = categorys_list
    context = {'user_details':user_details,'user_posts':datas,'categorys':category,'follows':follow}
    return render(request,'home.html',context)

#--------------------------------- User Profile --------------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def userProfile(request):
  # -----------------------------  Profile path -------------------------------------------------------  
    profileof = Websiteuser.objects.get(webuser=request.user)
    context = {"profileof":profileof}

  # -------------------------------- my posts------------------------------------------------------------
    if request.path == '/quilfoo/profile/my-posts/':
        postbyuser = UserPost.objects.filter(postby=profileof).order_by('-created_at')
        context = {"profileof":profileof,"postbyuser":postbyuser}

  # ----------------------------------my questions--------------------------------------------------------
    elif request.path == '/quilfoo/profile/my-questions/':  
        questionsbyuser = UserQuestion.objects.filter(questionby=profileof).order_by('-created_at')
        print("questionsbyuser-----------",questionsbyuser)
        context = {"profileof":profileof,"questionsbyuser":questionsbyuser}

  # ----------------------------------MY ANSWER ----------------------------------------------------------
    elif request.path == '/quilfoo/profile/my-answers/': 
        answerbyuser = AnswerQuestion.objects.filter(answerby=profileof).order_by('-created_at')
        print("answerbyuser-----------",answerbyuser)
        context = {"profileof":profileof,"answerbyuser":answerbyuser}  

    return render(request,'pages/myprofile/profile.html',context)


def otheruserProfile(request,pk):
    profileof = Websiteuser.objects.get(webuser=pk)
    postbyuser = UserPost.objects.filter(postby=profileof)
    questionsbyuser = UserQuestion.objects.filter(questionby=profileof)
    answerbyuser = AnswerQuestion.objects.filter(answerby=profileof)
    context = {"profileof":profileof,"postbyuser":postbyuser,"questionsbyuser":questionsbyuser,"answerbyuser":answerbyuser}
    return render(request,'myprofile/otherprofile.html',context)


def editUserProfile(request):
    profileof = Websiteuser.objects.get(webuser=request.user)
    errorIntext = {}
    form = WebsiteuserForm()
    form = WebsiteuserForm(instance=profileof)
    if request.method == "POST":
        form = WebsiteuserForm(request.POST,request.FILES , instance=profileof)             
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
        bio = request.POST.get('bio')
        currentpassword = request.POST.get('currentpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')

    # -------------------------------Validation--------------------------------------
        if name =="":
            errorIntext['name'] = 'Please, enter your name!'            
        if username =="":
            errorIntext['username'] = 'Please enter a username.'                
        if email =="":
            errorIntext['email'] = 'Please Enter the Email'
        elif email != "":
            if '@' and '.com' not in email:
                errorIntext['email'] = 'please enter a valid email'
        if phone != "":
            if not phone.isdigit():
                errorIntext['phone'] = 'Please enter a valid phone number'
            elif len(phone)<10:
                errorIntext['phone'] = 'Please enter a valid phone number'
        print("errorIntext",errorIntext)
        if errorIntext == {}:
            if currentpassword:
                if check_password(currentpassword, user.password):
                    if newpassword == confirmpassword:
                        hashed_password = make_password(newpassword)
                    else:
                        errorIntext['password'] ="New password does not match with Confirm Password"
                else:
                    errorIntext['password'] = 'Please enter your correct current password'
        # Update User model
            user = User.objects.get(username=request.user.username)
            user.first_name = name
            user.username = username
            user.email = email
            if currentpassword:
                if hashed_password:
                    user.password = hashed_password
            user.save()
            # Update Websiteuser model
            profileof.webuser = user
            profileof.phonefield = phone
            profileof.location = location
            profileof.linkedin = linkedin
            profileof.quora = quora
            profileof.reddit = reddit
            profileof.facebook = facebook
            profileof.twitter = twitter
            profileof.instagram = instagram
            if profilepic:
                profileof.profilepic = profilepic
            if coverpic:    
                profileof.coverpic = coverpic
            profileof.shortbio = shortbio
            profileof.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {"profiledetail":profileof,"errorIntext":errorIntext,"form":form}
    return render(request,'pages/myprofile/editprofile.html',context)













