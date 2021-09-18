from django.urls import path
from .views import CreateUser, ActivateUser, LoginUser, LogoutView, CheckAuth, ForgetPassword, RequestForgetPassword, \
    CreateWorkSpace,AddMembersWorkSpace

urlpatterns = [
    path('signup/', CreateUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('verify/', ActivateUser.as_view()),
    path('logout/', LogoutView.as_view()),
    path('check/auth/', CheckAuth.as_view()),
    path('forget/password/', ForgetPassword.as_view()),
    path('request/forget/password/', RequestForgetPassword.as_view()),
    path('create/workspace/', CreateWorkSpace.as_view()),
    path('add/members/', AddMembersWorkSpace.as_view()),
]