from django.urls import include, path
from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('question/', views.QuestionList.as_view()),
    path('question/<str:slug>/', views.QuestionDetail.as_view()),
    path('answer_create/<int:pk>/', views.answer_create),
    path('answer/<int:pk>/', views.AnswerDetail.as_view()),
    path('upvote_ques/<int:pk>/', views.upvote_ques),
    path('downvote_ques/<int:pk>/', views.downvote_ques),
    path('upvote_ans/<int:pk>/', views.upvote_ans),
    path('downvote_ans/<int:pk>/', views.downvote_ans),
    path('profile/', views.ProfileList.as_view()),
    path('profile/<str:username>/', views.ProfileDetail.as_view()),
    path('searched_ques/<str:searched_ques>', views.searched_ques)
]