from django.contrib import admin
from .models import Questions,UserQuestions,QuestionsOptions
# Register your models here.

# admin.site.register(Post)
admin.site.register(Questions)
admin.site.register(UserQuestions)
admin.site.register(QuestionsOptions)
