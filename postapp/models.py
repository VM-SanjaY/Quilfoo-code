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

class UserPost(models.Model):
    postby = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    description = RichTextUploadingField(config_name='default',null=True,blank=True)
    report_count = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    
class Postimage(models.Model):
    userpostid = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_file_path,blank=True,null=True,max_length=500)
    file_type = models.SmallIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class UserPostUpvoteDownvote(models.Model):
    userpostid = models.ForeignKey(UserPost,related_name='children',null=True,blank=True,on_delete=models.CASCADE)
    voteby = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    Upvote = models.PositiveIntegerField(null=True,blank=True,default=0)
    downvote = models.PositiveIntegerField(null=True,blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    @register.filter
    def in_category(things, Upvote):
        return things.filter(Upvote=Upvote)

class Comment(models.Model):
    userpostid = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    commentwriter = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    commentdetail = models.CharField(max_length=1000, null=True,blank=True)
    Upvote = models.PositiveIntegerField(null=True,blank=True)
    downvote = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class CommentReply(models.Model):
    mainpostid = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    Commentid = models.ForeignKey(Comment,related_name='children', on_delete=models.CASCADE)
    commentreplyuser = models.ForeignKey(Websiteuser, null=True, blank=True, on_delete=models.CASCADE)
    commentdetail = models.CharField(max_length=1000, null=True, blank=True)
    Upvote = models.PositiveIntegerField(null=True, blank=True)
    downvote = models.PositiveIntegerField(null=True, blank=True)
    subreplyof = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_replies')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return f"CommentReply #{self.id}"
    
class Reportpost(models.Model):
    reported_on = models.ForeignKey(UserPost,null=True,blank=True,on_delete=models.CASCADE)
    reported_by = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    complaintonpost = models.CharField(max_length=550,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)