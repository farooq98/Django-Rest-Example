from django.urls import path
from .views import GetAllUsersWithQuiz,QuestionView,QuizAnswerAPIView,LeaderBoard

urlpatterns = [
    path('users/quiz/', GetAllUsersWithQuiz.as_view()),
    path('questionare/', QuestionView.as_view()),
    path('answer/quiz/', QuizAnswerAPIView.as_view()),
    path('leaderboard/', LeaderBoard.as_view()),
]