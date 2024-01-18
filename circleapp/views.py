from django.shortcuts import render,redirect
from loginapp.models import *
from django.db.models import Q
from .models import *
from .forms import *
# Create your views here.



def circlepage(request):
    groups = Circle.objects.filter().order_by('membercount','-updated_at')
    grouplist = ""
    if request.user.is_authenticated:
        siteuser = Websiteuser.objects.get(webuser=request.user)
        grouplist=[]
        groupdata = MembersinCircle.objects.filter(member=siteuser)
        for gdata in groupdata:
            grouplist.append(gdata.circleinfo.id)
        if request.method =="POST":
            member = request.POST.get('member')
            groupcode = request.POST.get('group_id')
            groupid = Circle.objects.get(id=groupcode)
            print(groupid.titleheader)
            alreadymem = MembersinCircle.objects.filter(member=siteuser, circleinfo=groupid).exists()
            if alreadymem == False:
                if member == 'yes':
                    data = MembersinCircle(circleinfo=groupid,member=siteuser)
                    data.save()
                    return redirect('circlepage')
            elif alreadymem == True:
                if member == "nope":
                    print("groupid.id --", groupid.id)
                    MembersinCircle.objects.filter(circleinfo=groupid.id).delete()
                    return redirect('circlepage')

    context =  {"groups":groups,"grouplist":grouplist}
    return render(request,'circle.html',context)

def createCircle(request):
    if request.user.is_authenticated:
        siteuser = Websiteuser.objects.get(webuser=request.user) 
        form = CircleForm()
        if request.method == "POST":
            form = CircleForm(request.POST,request.FILES)
            if form.is_valid():
                dep = request.POST.get('description')
            try:
                dep = dep
            except:
                dep = None
            name = request.POST.get('name')
            image = request.Files.get('topicimage')
            try:
                image = image
            except:
                image = None
            if name:
                data = Circle(
                    owner = siteuser,
                    titleheader = name,
                    description = dep,
                    image = image
                )
                data.save()
                return redirect('circlepage')
        context = {"form":form}
        return render(request,'creategroup.html',context)
    else:
        return redirect('/')



def circlemember(request,pk):
    circledata = Circle.objects.get(pk=pk)
    memdata = MembersinCircle.objects.filter(circleinfo=pk)
    if request.user.is_authenticated:
        siteuser = Websiteuser.objects.get(webuser=request.user)
        follwlist = Websiteuser.user.filter(user=siteuser)
        listofFollwers = []
        for followers in follwlist:
            listofFollwers.append(followers.following)
        print("listofFollwers --",listofFollwers)


    return render(request,'circlemember.html')