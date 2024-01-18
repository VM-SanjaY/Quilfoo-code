from django.urls import path
from . import views
urlpatterns = [
    path('',views.addPost,name='addPost'),
    path('my-post/',views.myPost,name='myPost'),
    path('edit-post/<id>',views.postEdit,name="postEdit"), 
    path('delete-post/<id>',views.postDelete,name="postDelete"), 
    path('like-post/',views.likePost,name="likePost"),
    path('unlike-post/',views.unlikePost,name="unlikePost"),
    path('post-comment/<id>',views.postComment,name="postComment"),
    path('post-comment-delete/<id>',views.postCommentDelete,name="postCommentDelete"),
    path('post-comment-reply/<id>',views.postCommentReply,name="postCommentReply"),
    path('post-comment-reply-delete/<id>',views.postCommentReplyDelete,name="postCommentReplyDelete"),
]