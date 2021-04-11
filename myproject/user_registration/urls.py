from django.urls import path
from .views import CreateUser, ActivateUser

urlpatterns = [
    path('signup/', CreateUser.as_view()),
    path('verify/', ActivateUser.as_view()),
]