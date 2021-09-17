from django.db import models
from .custom_user_model import UserModel
# Create your models here.


class WorkSpaceModel(models.Model):

    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    workspace_name = models.CharField(max_length=50)
    workspace_image = models.ImageField()


class UserWorkSpaceRelationTable(models.Model):

    user_choices = (
        ('normal', 'Normal User'),
        ('admin', 'Admin User')
    )

    user_id = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    workspace_id = models.ForeignKey(WorkSpaceModel,on_delete=models.CASCADE)
    type_of_user = models.CharField(max_length=10,choices=user_choices)