from django.urls import path
from .views import GetAllUsersWithQuiz,QuestionView,QuizAnswerAPIView

urlpatterns = [
    path('users/quiz/', GetAllUsersWithQuiz.as_view()),
    path('questionare/', QuestionView.as_view()),
    path('answer/quiz/', QuizAnswerAPIView.as_view()),
]