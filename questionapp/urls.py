from django.urls import path
from . import views


urlpatterns = [
    path('ask/',views.questionPage,name="questionPage"),
    path('question-list/',views.listOfQuestion,name="listquestion"),
    path('answer/<str:pk>/',views.answerpage,name = "answerpage"),
    path("your-answers/",views.answerByYou,name="answerByYou"),
    path("your-questions/",views.questionByYou,name="questionByYou"),
    path("all-answers/",views.listAnswers,name = "listAnswers"),
    path('answer/detail/<str:pk>/',views.detailofAnswer,name="detailofAnswer"),
]
    