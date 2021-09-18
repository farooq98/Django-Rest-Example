from rest_framework import serializers
from .models import Post, Comment, Like



class CommentSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'created_at', 'email']
    
class LikeSerializer(serializers.ModelSerializer):
    
    email = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['email']
    
class PostSerializer(serializers.ModelSerializer):
    
    created_by = serializers.ReadOnlyField(source='user.name')
    email = serializers.ReadOnlyField(source='user.username')
    commented_by = CommentSerializer(source='comments', many=True, read_only=True)
    liked_by = LikeSerializer(source='likes', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'image_url', 
            'content',
            'created_at', 
            'edited_at',
            'workspace',
            'created_by', 
            'email',
            'liked_by', 
            'commented_by', 
        ]
