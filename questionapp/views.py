from django.shortcuts import render,redirect
from loginapp.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


def questionPage(request):
    if request.method == "POST":
        question = request.POST.get('question')
        if question:
            print(question)
            data = UserQuestion(
                questionby = request.user,
                ask = question
            )
            data.save()
            return redirect('userHome')
    return render(request,'questionpage.html')

def listOfQuestion(request):
    siteuser = Websiteuser.objects.get(webuser=request.user)
    listquestion = UserQuestion.objects.all().exclude(questionby=siteuser).order_by('-id')
    context = {"listquestion":listquestion}
    return render(request,'listquestion.html',context)


# @login_required(login_url="userLoginpage")
# @user_login()
def answerpage(request,pk):
    question = UserQuestion.objects.get(pk=pk)
    siteuser = Websiteuser.objects.get(webuser=request.user)
    if request.method == "POST":
        answer = request.POST.get('answer')
        imageinfo = request.FILES.getlist('filedata[]')
        print("sezhzsdrh",imageinfo)
        if answer:
            if AnswerQuestion.objects.filter(Q(questionform = question)&Q(answerby = siteuser)).exists():
                messages.info(request,"You have already answered this Question")
            else:    
                data = AnswerQuestion(
                    questionform = question,
                    answerby = siteuser,
                    description = answer
                )
                data.save()
                datainanswer = AnswerQuestion.objects.filter(answerby=siteuser).last()
                print('rgnnjrdsrh',datainanswer)
                print("questionform", data.questionform,"answerby",data.answerby,"description",data.description)
                if imageinfo:
                    print("imageinfo",imageinfo)
                    for imagein in imageinfo:
                        print("imageinimagein",imagein)
                        get_extension = str(imagein)
                        if '.mp4' in get_extension:
                            file_type = 1
                        else:
                            file_type = 0
                        imagdata = ImageonAnswer(useranswerid = datainanswer,image = imagein)
                        AnswerQuestion.objects.get(id=datainanswer).update(file_type=file_type)
                        imagdata.save()
            
    context = {"question":question}
    return render(request,'answerpage.html',context)


# -------------------------- Question by you and answer by you page ------------------------------

# @login_required(login_url="userLoginpage")
# @user_login()
def questionByYou(request):
    siteuser = Websiteuser.objects.get(webuser=request.user)
    yourquestion = UserQuestion.objects.filter(questionby=siteuser).order_by('-id')
    context = {"yourquestion":yourquestion}
    return render(request,'questionbyyou',context)



# @login_required(login_url="userLoginpage")
# @user_login()
def answerByYou(request):
    siteuser = Websiteuser.objects.get(webuser=request.user)
    youranswer = AnswerQuestion.objects.filter(answerby=siteuser).order_by('-id')
    context = {"youranswer":youranswer}
    return render(request,'answerbyyou.html',context)

# ------------------------- complete question and answer page ----------------------------

def listAnswers(request):
    allanswer = AnswerQuestion.objects.all().order_by('-id')
    context = {"allanswer":allanswer}
    return render(request,'allanswers.html',context)



def detailofAnswer(request,pk):    
    qanda = AnswerQuestion.objects.get(id=pk)
    imageinanswer = ImageonAnswer.objects.filter(useranswerid=pk).order_by('-id')
    comments = Commentonanswer.objects.filter(useranswerid=pk).order_by('-id')
    replys = ReplyonCommentanswer.objects.filter(mainanswerid=pk).order_by('id')
    if request.user.is_authenticated:
        siteuser = Websiteuser.objects.get(webuser=request.user)
        if request.method == "POST":
            commentget = request.POST.get('comment')
            commentimage = request.FILES.getlist('commentimage[]')
            print("commentimage",commentimage)
            replyget = request.POST.get('reply')
            replyimage = request.FILES.getlist('replyimage[]')
            replyget2 = request.POST.get('reply2')
            replyimage2 = request.FILES.getlist('replyimage[]')
            replyget3 = request.POST.get('reply3')
            replyimage3 = request.FILES.getlist('replyimage[]')
            comment_id = request.POST.get('parent_comment_id')
            if comment_id:
                comment_instance = Commentonanswer.objects.get(id=comment_id)
            reply_id = request.POST.get('parent_reply_id')
            if reply_id:
                reply_instance = ReplyonCommentanswer.objects.get(id=reply_id)

            if commentget:
                commentdata = Commentonanswer(useranswerid=qanda,commentanswerwriter=siteuser,commentanswerdetail=commentget)
                commentdata.save()
            if commentimage:
                print("yessss")
                get_extension = str(commentimage)
                print("get_extension",get_extension)
                if '.jpg' or '.png' or '.jpeg' in get_extension:
                    commentfrom = Commentonanswer.objects.filter(commentanswerwriter=siteuser).last()

                else:
                    messages.info(request,'you can add only images in the comment section')
                    return redirect('detailofAnswer', id=pk )
            if replyget:
                replydata = ReplyonCommentanswer(mainanswerid=qanda,Commentanswerid=comment_instance,commentanswerreplyuser=siteuser,
                                                 replydetail=replyget)
                replydata.save()
                if replyimage:
                    get_extension = str(replyimage)
                    if '.jpg' or '.png' or '.jpeg' in get_extension:
                        replyfrom = ReplyonCommentanswer.objects.filter(commentanswerreplyuser=siteuser).last()

                    else:
                        messages.info(request,'you can add only images in the reply section')
                        return redirect('detailofAnswer', id=pk )

            if replyget2:
                replydata = ReplyonCommentanswer(mainanswerid=qanda,Commentanswerid=comment_instance,commentanswerreplyuser=siteuser,
                                                 replydetail=replyget,subreplyofanswer=reply_instance)
                replydata.save()
                if replyimage2:
                    get_extension = str(replyimage2)
                    if '.jpg' or '.png' or '.jpeg' in get_extension:
                        replyfrom = ReplyonCommentanswer.objects.filter(commentanswerreplyuser=siteuser).last()

                    else:
                        messages.info(request,'you can add only images in the reply section')
                        return redirect('detailofAnswer', id=pk )
            if replyget3:
                replydata = ReplyonCommentanswer(mainanswerid=qanda,Commentanswerid=comment_instance,commentanswerreplyuser=siteuser,
                                                 replydetail=replyget,subreplyofanswer=reply_instance)
                replydata.save()
                if replyimage3:
                    get_extension = str(replyimage3)
                    if '.jpg' or '.png' or '.jpeg' in get_extension:
                        replyfrom = ReplyonCommentanswer.objects.filter(commentanswerreplyuser=siteuser).last()


    context ={"qanda":qanda,"imageinanswer":imageinanswer,"comments":comments,"replys":replys}
    return render(request,'detailofAnswer.html',context)
    
# -----------------------------------------------------------------------------------------------------------------------
