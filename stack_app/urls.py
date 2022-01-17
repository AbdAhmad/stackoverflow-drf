from django.urls import path
from . import views


urlpatterns = [
    path('question/', views.QuestionList.as_view()),
    path('question/<str:slug>/', views.QuestionDetail.as_view()),
    path('answer_create/<int:pk>/', views.AnswerCreate.as_view()),
    path('answer/<int:pk>/', views.AnswerDetail.as_view()),
    path('upvote_ques/<int:pk>/', views.UpvoteQues.as_view()),
    path('downvote_ques/<int:pk>/', views.DownvoteQues.as_view()),
    path('upvote_ans/<int:pk>/', views.UpvoteAns.as_view()),
    path('downvote_ans/<int:pk>/', views.DownvoteAns.as_view()),
    path('profile/', views.ProfileList.as_view()),
    path('profile/<str:username>/', views.ProfileDetail.as_view()),
    path('searched_ques/<str:searched_ques>', views.SearchedQues.as_view())
]