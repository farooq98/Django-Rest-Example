from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')
    likes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'image_url', 'content', 'likes', 'created_at', 'edited_at', 'email']

class CommentSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'created_at', 'email']
