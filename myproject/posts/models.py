from django.db import models
from user_registration.models import UserModel, WorkSpaceModel


class Post(models.Model):

    user = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    workspace = models.ForeignKey(WorkSpaceModel, on_delete = models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    likes = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="comments")
    user = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    content = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

