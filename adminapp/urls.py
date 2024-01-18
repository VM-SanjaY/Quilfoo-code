from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin,name="loginpage"),
    path('logoutpage/',views.adminlogout,name="adminlogoutpage"),
    path('home/',views.adminhome,name = 'adminhome'),
    path('user-table/',views.adminusertable,name="adminusertable"),
    path('user-table/edit/<str:pk>/',views.editadminusertable,name="editadminusertable"),
    path('temporary-table/',views.admintemporarytable,name="admintemporarytable"),
    path('temporary-table/edit/<str:pk>/',views.editadmintemporarytable,name="editadmintemporarytable"),
    path('profile/edit/<str:pk>/',views.editadminprofile,name ="editadminprofile"),
    path('profile/<str:pk>/change-password/',views.changePasswordAdmin,name="changepasswordadmin"),
    path('profile/<str:pk>/',views.adminprofile, name ="adminprofile"),
    path('report-post/',views.reportPost,name="reportPost"),
    path('report-post-user/<str:pk>',views.reportPostUser,name="reportPostUser"),
    path('categories/',views.category,name="category"),
    path('categories/add/',views.addCategory,name="addcategory"),
    path('categories/edit/<str:pk>',views.editCategory,name="editcategory"),
    path("maps/",views.userLocateMap,name="usermap"),
    path('notification/',views.adminNotification,name="adminNotification"),
    path('notification/<str:pk>',views.adminMessageOfNoti,name="adminnotifyMessagepage"),
    path('Terms-Conditions/',views.agreementpage,name="agreementpage"),
    path('Terms-Conditions/edit/',views.editAgreementpage,name="editAgreementpage"),
    path('reportAnswer/',views.reportAnswer,name="reportanswer"),
    path('reportAnswer/info/<str:pk>/',views.reportAnsweruser,name="reportansweruser"),
]


