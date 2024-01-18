from django.urls import path
from . import views

urlpatterns = [
    path('',views.circlepage,name="circlepage"),
    path('create/',views.createCircle,name="createCircle"),
    path('members/<str:pk>/',views.circlemember,name="circlemember")
]
    