from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
# Create your models here.


class Temperorytable(models.Model):
    name = models.CharField(max_length=250,null = True, blank=True)
    email = models.CharField(max_length=250,null = True, blank=True)
    username = models.CharField(max_length=250,null = True, blank=True)
    password = models.CharField(max_length=250,null = True, blank=True)
    phonefield = models.CharField(max_length=250,null = True, blank=True)
    otp = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.name



class Websiteuser(models.Model):
    webuser = models.OneToOneField(User, null = False, blank = False, on_delete=models.CASCADE)
    phonefield = models.CharField(max_length=20,null = True, blank=True)
    location = models.CharField(max_length=200,null = True, blank=True)
    profilepic = models.ImageField(upload_to="userdetail/profilepic/", max_length=200,blank=True,default="userdetail/profilepic/gokussj.png")
    coverpic = models.ImageField(upload_to="userdetail/coverpic/", max_length=200,blank=True,default="userdetail/coverpic/ivancik.jpg")
    report_count = models.SmallIntegerField(null = True,blank=True)
    bio = RichTextUploadingField(null = True, blank=True)
    shortbio = models.CharField(max_length=500,null = True, blank=True)
    interest_category = models.CharField(max_length=500,null=True,blank=True)
    linkedin = models.URLField(max_length=250,null = True, blank=True)
    quora = models.URLField(max_length=250,null = True, blank=True)
    reddit = models.URLField(max_length=250,null = True, blank=True)
    facebook = models.URLField(max_length=250,null = True, blank=True)
    twitter = models.URLField(max_length=250,null = True, blank=True)
    instagram = models.URLField(max_length=250,null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.webuser.username

class Follower(models.Model):
    webuserid = models.ForeignKey(Websiteuser,related_name='user',null=True,blank=True, on_delete=models.CASCADE)
    following = models.ForeignKey(Websiteuser,related_name='following',null=True,blank=True,on_delete=models.CASCADE)
    # follower = models.ForeignKey(Websiteuser,related_name='follower',null=True,blank=True,default=0, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class Circle(models.Model):
    owner = models.ForeignKey(Websiteuser,null=True,blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="group/",blank=True,null=True)
    titleheader = models.CharField(max_length=550,null=True,blank=True)
    description = RichTextUploadingField(config_name='detail',null=True,blank=True)
    membercount = models.PositiveIntegerField(default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)



class MembersinCircle(models.Model):
    circleinfo = models.ForeignKey(Circle,null=True,blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey(Websiteuser,null=True,blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


