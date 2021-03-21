from django.urls import path
from .views import Test, TestCreate, SendMessagesOnEmail

urlpatterns = [
    path('test/', Test.as_view()),
    path('test/create/', TestCreate.as_view()),
    path('test/sendemail/', SendMessagesOnEmail.as_view())
]
