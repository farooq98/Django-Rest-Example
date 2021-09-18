from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'image_url', 'content', 'likes', 'created_at', 'updated_at', 'email']

class CommentSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'created_at']
