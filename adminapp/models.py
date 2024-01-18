from django.db import models
from loginapp.models import Websiteuser
from ckeditor_uploader.fields import RichTextUploadingField
import uuid 
# Create your models here.

class Message(models.Model):
    fromwho = models.ForeignKey(Websiteuser,blank=True,null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=250,blank=True,null=True)
    description = RichTextUploadingField(blank=True,null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class AgreementData(models.Model):
    creaby = models.ForeignKey(Websiteuser, blank=True, null=True, on_delete=models.CASCADE)
    description = RichTextUploadingField(config_name='agreem', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


