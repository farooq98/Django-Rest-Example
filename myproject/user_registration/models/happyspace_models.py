from django.db import models
from .custom_user_model import UserModel
# Create your models here.


class WorkSpaceModel(models.Model):

    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    workspace_name = models.CharField(max_length=50)
    workspace_image = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.workspace_name


class UserWorkSpaceRelationTable(models.Model):

    USER_CHOICES = (
        ('normal', 'Normal User'),
        ('admin', 'Admin User')
    )

    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpaceModel,on_delete=models.CASCADE)
    type_of_user = models.CharField(max_length=10,choices=USER_CHOICES, null=True)

    def __str__(self):
        return self.workspace.workspace_name

    def __save__(self, *args, **kwargs):
        if not self.type_of_user:
            self.type_of_user = self.USER_CHOICES[0][0]
        super().save(*args, **kwargs)