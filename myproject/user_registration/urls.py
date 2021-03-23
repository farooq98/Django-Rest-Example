from django.urls import path
from .views import CreateUser

urlpatterns = [
    path('signup/', CreateUser.as_view()),
]