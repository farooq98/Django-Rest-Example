from django.urls import path
from .views import GetAllUsersWithQuiz

urlpatterns = [
    path('users/quiz/', GetAllUsersWithQuiz.as_view())
]