from django.db import models
from loginapp.models import Websiteuser
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
import os
from django import template
register = template.Library()
# Create your models here.

#-------------- Generate unique file name -----------------
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('write/post/', filename)



# ------------------------------------------------------------------------------------

class Category(models.Model):
    topic = models.CharField(max_length=150,blank=True,null=True)
    image = models.ImageField(upload_to="topic/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class CategoryFollower(models.Model):
    webuserid = models.ForeignKey(Websiteuser,null=True,blank=True, on_delete=models.CASCADE)
    categoryid = models.ForeignKey(Category,null=True,blank=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class Notification(models.Model):
    fromuser=models.ForeignKey(Websiteuser,null=True,blank=True, on_delete=models.SET_NULL)
    touser = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.SET_NULL,related_name = "messages")
    title = models.CharField(max_length=250,null=True,blank=True)
    detaildesc = RichTextUploadingField(config_name='detail',null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


