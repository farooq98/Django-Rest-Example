from django.urls import path
from .views import GetAllUsersWithQuiz,QuestionView

urlpatterns = [
    path('users/quiz/', GetAllUsersWithQuiz.as_view()),
    path('questionare/', QuestionView.as_view()),
]