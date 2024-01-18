from django.urls import path
from . import views
urlpatterns = [
    path('categorys/',views.category,name='userCategory'),
    path('',views.home,name='userHome'),
    path('profile/',views.userProfile,name='userProfile'),
    path('profile/my-posts/',views.userProfile,name ="profilepost"),
    path('profile/my-questions/',views.userProfile,name ="profilequestion"),
    path('profile/my-answers/',views.userProfile,name ="profileanswer"),
    path('profile/edit',views.editUserProfile,name='edituserprofile'),
    path('user-profile/<str:pk>/',views.otheruserProfile,name='otheruserProfile'),
    path('follow-unfollow/',views.followUnfollow,name="followUnfollow"),

]