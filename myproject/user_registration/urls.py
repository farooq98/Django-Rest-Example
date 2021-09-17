from django.urls import path
from .views import CreateUser, ActivateUser, LoginUser, LogoutView, CheckAuth, ForgetPassword

urlpatterns = [
    path('signup/', CreateUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('verify/', ActivateUser.as_view()),
    path('logout/', LogoutView.as_view()),
    path('check/auth/', CheckAuth.as_view()),
    path('forget/password/', ForgetPassword.as_view()),
]