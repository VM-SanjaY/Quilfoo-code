from django.shortcuts import render
from .forms import UserPostForm,WebsiteuserForm
from django.contrib.auth.decorators import login_required
from Quilfoo.decorators import *
from loginapp.models import *
from .models import *
from django.http import JsonResponse
import json
# Create your views here.
#--------------------------------- User Add Post --------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def addPost(request):
    form = UserPostForm()
    if request.method=='POST':
        # form = UserPostForm(request.POST,request.FILES) 
        description = request.POST.get('description')
        post_file = request.FILES.getlist('post_file[]')     
        if description =='' and post_file==[]:
            messages.warning(request,'Empty post not accepted')
        else:
            user_id = Websiteuser.objects.get(webuser=request.user)
            user_post = UserPost(postby = user_id,description = description)
            user_post.save()
            post_id = UserPost.objects.filter(postby = user_id.id).last()
            for post_item in post_file:
                get_extension = str(post_item)
                if '.mp4' in get_extension:
                    file_type = 1
                else:
                    file_type = 0
                post_file = Postimage(userpostid = post_id,image = post_item,file_type=file_type)
                post_file.save()
    return render(request,'post.html',{'form':form})

#--------------------------------- User Post List --------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def myPost(request):
    temp = []
    datas =[]
    user = Websiteuser.objects.get(webuser_id = request.user)
    user_posts = UserPost.objects.filter(postby_id = user).order_by('-id')
    for i in user_posts:
        temp.append(i.id)
    for user_post_id in temp:
        user_post = UserPost.objects.get(id = user_post_id)
        print('vsd',user_post)
        datas.append(user_post)
    context = {'user_posts':datas}
    return render(request,'pages/myprofile/myPost.html',context)

#--------------------------------- User Post Edit --------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def postEdit(request,id):
    descriptionof = UserPost.objects.get(id=id)
    form = UserPostForm()
    datas = []
    if request.method=="POST":
        description = request.POST.get('description')
        post_file = request.FILES.getlist('post_file[]') 
        if description:
            user_post = UserPost.objects.get(id=id)
            print('sasisk',description,post_file)
            user_post.description = description
            user_post.save()
            post_id = UserPost.objects.get(id = id)
            print('done') 
        for post_item in post_file:
                get_extension = str(post_item)
                if '.mp4' in get_extension:
                    file_type = 1
                else:
                    file_type = 0
                post_file = Postimage(userpostid = post_id,image = post_item,file_type=file_type)
                post_file.save() 
    user_posts = UserPost.objects.get(id = id)
    form = UserPostForm(instance=user_posts)
    user_post_img = Postimage.objects.filter(userpostid_id = user_posts.id ).order_by('-id')
    context = {'user_description':user_posts,'user_posts':user_post_img,'form':form}
    return render(request,'pages/myprofile/editMyPost.html',context)

#--------------------------------- User Post Delete --------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def postDelete(request,id):
    if 'quilfoo/post/edit-post/' in request.META.get('HTTP_REFERER'):
        user_post = Postimage.objects.get(id=id)
        user_post.delete()
        print(id)
    else:
        user_post = UserPost.objects.get(id=id)
        user_post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#--------------------------------- User Post Upvote --------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def likePost(request):
    print('hihihihi')
    up_vote=0
    down_vote=0
    post_id = request.GET['post_id']
    user_id = Websiteuser.objects.get(webuser_id = request.user)
    data = UserPostUpvoteDownvote.objects.filter(userpostid_id = post_id,voteby_id=user_id)
    if data:
        like = UserPostUpvoteDownvote.objects.get(userpostid_id = post_id,voteby_id=user_id)
        if like.downvote ==1:
            down_vote=0
            if like.Upvote == 0:
                up_vote =1
        elif like.downvote ==0:
            down_vote=0
            if like.Upvote == 1:
                up_vote = 0
            else:
                up_vote =1
        data.update(Upvote=up_vote,downvote = down_vote)
    else:
        data = UserPostUpvoteDownvote(
            Upvote = 1,
            userpostid_id = post_id,
            voteby_id = user_id.id
        )
        data.save()
    like = UserPostUpvoteDownvote.objects.filter(userpostid_id = post_id,Upvote = 1).count()
    unlike = UserPostUpvoteDownvote.objects.filter(userpostid_id = post_id,downvote = 1).count()
    return JsonResponse({"id" : post_id,
                        "upvote" : like,
                        "downvote": unlike}, status=200)

#--------------------------------- User Post Downvote --------------------------------------------------
@login_required(login_url="userLoginpage")
@user_login()
def unlikePost(request):
    up_vote=0
    down_vote=0
    post_id = request.GET['post_id']
    user_id = Websiteuser.objects.get(webuser_id = request.user)
    data = UserPostUpvoteDownvote.objects.filter(userpostid_id = post_id,voteby_id=user_id)
    if data:
        unlike = UserPostUpvoteDownvote.objects.get(userpostid_id = post_id,voteby_id=user_id)
        if unlike.Upvote ==1:
            up_vote=0
            if unlike.downvote == 0:
                down_vote =1
        elif unlike.Upvote ==0:
            if unlike.downvote == 1:
                down_vote = 0
            else:
                down_vote =1
        data.update(Upvote=up_vote,downvote = down_vote)
    else:
        data = UserPostUpvoteDownvote(
            downvote = 1,
            userpostid_id = post_id,
            voteby_id = user_id.id
        )
        data.save()
    like = UserPostUpvoteDownvote.objects.filter(userpostid_id = post_id,Upvote = 1).count()
    unlike = UserPostUpvoteDownvote.objects.filter(userpostid_id = post_id,downvote = 1).count()
    return JsonResponse({"id" : post_id,
                        "upvote" : like,
                        "downvote": unlike}, status=200)
    
#-------------------------------- User Post Comment --------------------------------------------
def postComment(request,id):
    if request.method=="POST":
        print(list(request.POST.keys())[1])
        print(id)
        comment_name = list(request.POST.keys())[1]
        comment_value = request.POST.get(comment_name)
        user_id = Websiteuser.objects.get(webuser_id=request.user.id)
        if comment_name =='comment':
            data = Comment(commentdetail=comment_value,commentwriter_id=user_id.id,userpostid_id=id)
            data.save()
            print('55',comment_value)
        else:
            print(comment_name)
            data = CommentReply(commentdetail=comment_value,Commentid_id=int(comment_name),mainpostid_id=id,commentreplyuser_id=user_id.id)
            data.save()
            print('gsdf')
    # comments = Comment.objects.filter(userpostid=id)
    comment_user = Comment.objects.filter(userpostid=id).prefetch_related("children")
    comments =[]
    for p in comment_user:
        parent_data = {"id": p.pk, "description": p.commentdetail,'name':p.commentwriter,'profile':p.commentwriter.profilepic}
        parent_data["replys"] = CommentReply.objects.filter(Commentid_id = p.pk,subreplyof_id=None)
        parent_data["sub_replys"] = CommentReply.objects.filter(Commentid_id = p.pk,subreplyof_id__isnull= False).order_by('subreplyof_id')
        comments.append(parent_data)
    print(comments)
    context ={'comments':comments}
    return render(request,'comment.html',context)
# --------------------------------- User Post Comment Reply --------------------------------------------------
def postCommentReply(request,id):
    if request.method=="POST":
        comment_reply = CommentReply.objects.get(id=id)
        user_id = Websiteuser.objects.get(id=request.user.id)
        comment_id = comment_reply.Commentid_id
        post_id = comment_reply.mainpostid_id
        comment_replay_name = list(request.POST.keys())[1]
        comment_replay_value = request.POST.get(comment_replay_name)
        print(id,comment_reply)
        data = CommentReply(commentdetail=comment_replay_value,Commentid_id=comment_id,commentreplyuser_id=user_id.id,mainpostid_id=post_id,subreplyof_id=id)
        data.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# --------------------------------- Delete User Post Comment --------------------------------------------------
def postCommentDelete(request,id):
    data=Comment.objects.get(id=id)
    if request.user.id == data.commentwriter_id:
        data.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# --------------------------------- Delete User Post Comment Reply --------------------------------------------------
def postCommentReplyDelete(request,id):
    data=CommentReply.objects.get(id=id)
    if request.user.id == data.commentreplyuser_id:
        data.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
