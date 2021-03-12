from django.urls import path
from .views import Test, TestCreate

urlpatterns = [
    path('test/', Test.as_view()),
    path('test/create/', TestCreate.as_view()),
]
