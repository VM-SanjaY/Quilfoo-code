from django.db import models
from loginapp.models import Websiteuser
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
import os


def get_file_pathforquestion(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('write/answer/', filename)


class UserQuestion(models.Model):
    questionby = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    ask = models.CharField(max_length=1050,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class AnswerQuestion(models.Model):
    questionform = models.ForeignKey(UserQuestion,null=True,blank=True,on_delete=models.CASCADE)
    answerby = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    description = RichTextUploadingField(config_name='default',null=True,blank=True)
    file_type = models.SmallIntegerField(null=True,blank=True)
    report_count = models.PositiveIntegerField(null=True,blank=True)
    Upvote = models.PositiveIntegerField(null=True,blank=True)
    downvote = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class ReportOnAnswer(models.Model):
    reported_on = models.ForeignKey(AnswerQuestion,null=True,blank=True,on_delete=models.CASCADE)
    reported_by = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    complaintonanswer = models.CharField(max_length=550,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class ImageonAnswer(models.Model):
    useranswerid = models.ForeignKey(AnswerQuestion,null=True,blank=True,on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_file_pathforquestion,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

class Commentonanswer(models.Model):
    useranswerid = models.ForeignKey(AnswerQuestion, on_delete=models.CASCADE)
    commentanswerwriter = models.ForeignKey(Websiteuser,null=True,blank=True,on_delete=models.CASCADE)
    commentanswerdetail = models.CharField(max_length=1000, null=True,blank=True)
    Upvote = models.PositiveIntegerField(null=True,blank=True)
    downvote = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


class ReplyonCommentanswer(models.Model):
    mainanswerid = models.ForeignKey(AnswerQuestion, on_delete=models.CASCADE)
    Commentanswerid = models.ForeignKey(Commentonanswer, on_delete=models.CASCADE)
    commentanswerreplyuser = models.ForeignKey(Websiteuser, null=True, blank=True, on_delete=models.CASCADE)
    replydetail = models.CharField(max_length=1000, null=True, blank=True)
    Upvote = models.PositiveIntegerField(null=True, blank=True)
    downvote = models.PositiveIntegerField(null=True, blank=True)
    subreplyofanswer = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_replies')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return f"CommentReply #{self.id}"
    
