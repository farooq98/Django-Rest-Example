from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = False

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Comment, CommentInline)
