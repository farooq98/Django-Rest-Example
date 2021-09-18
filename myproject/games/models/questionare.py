from django.db import models
from user_registration.models import UserModel

# Create your models here.


class Questions(models.Model):

    question = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=50)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)


class QuestionsOptions(models.Model):

    option_1 = models.CharField()
    option_2 = models.CharField()
    option_3 = models.CharField()
    option_4 = models.CharField()
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)