from django.db import models
from user_registration.models import UserModel

# Create your models here.


class Questions(models.Model):

    question = models.CharField(max_length=200)


class QuestionsOptions(models.Model):

    option_text = models.CharField(max_length=50)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='options')

class UserQuestions(models.Model):

    class Meta:
        unique_together = (('question', 'correct_answer', 'user'),)

    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    correct_answer = models.ForeignKey(QuestionsOptions, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='questions')