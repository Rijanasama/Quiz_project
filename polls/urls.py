
from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login_user,name="login"),
    path('', views.login_user, name="login"),
    path('api/get-quiz/',views.get_quiz,name="get_quiz"),
    path('quiz',views.quiz,name="quiz"),
    path('index',views.index,name = "index"),
    path('signup/',views.signup,name="signup"),
    path('log_out',views.log_out,name='logout'),
    path('score/',views.get_marks,name="score")
    # path('score/log_out',views.log_out,name="logout")
]
