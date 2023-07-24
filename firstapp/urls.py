from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('question/new/', views.CreateQuestionView.as_view(), name='add_question'),
    path('question/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('answer/<int:pk>/like/', views.like_comment, name='like_comment'),
]