from django.urls import path
from .views import GetAllUsersWithQuiz,QuestionView,QuizAnswer

urlpatterns = [
    path('users/quiz/', GetAllUsersWithQuiz.as_view()),
    path('questionare/', QuestionView.as_view()),
    path('answer_quiz/', QuizAnswer.as_view()),
]