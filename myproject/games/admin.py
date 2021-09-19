from django.contrib import admin
from .models import Questions, QuestionsOptions, UserQuestions
# Register your models here.

admin.site.register(Questions)
admin.site.register(QuestionsOptions)
admin.site.register(UserQuestions)
