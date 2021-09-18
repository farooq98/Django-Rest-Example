from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'image_url', 'content', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'content', 'created_at']
