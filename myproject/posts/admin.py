from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    inlines = (CommentInline, Like)

# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post, PostAdmin)
