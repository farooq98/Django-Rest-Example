from rest_framework.pagination import PageNumberPagination
from core.authentication import PrivateAPI, PrivateListAPI
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer
from rest_framework import status

from .models import Post, Comment, Like
from user_registration.models import WorkSpaceModel, UserWorkSpaceRelationTable

# Create your views here.

def validate_user_and_workspace(request):
    try:
        return UserWorkSpaceRelationTable.objects.get(
            workspace__id = request.data.get('workspace_id'), 
            user = request.user
        )
    except WorkSpaceModel.DoesNotExist:
        return Response({
            "status": False,
            "message": "Invalid workspace"
        }, status=status.HTTP_400_BAD_REQUEST)

class PostView(PrivateAPI):

    def put(self, request):
        
        workspace_obj = validate_user_and_workspace(request)

        if isinstance(workspace_obj, Response):
            return workspace_obj

        post = {
            'user': request.user,
            'workspace': workspace_obj.workspace,
            'content': request.data.get('content'),
            'image_url': request.data.get('image_url'),
        }

        post_obj = Post.objects.create(**post)

        return Response({
            "status": True,
            "message": "post created",
            "post_id": post_obj.id
        }, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            post_obj = Post.objects.get(pk=request.data.get('post_id'), user=request.user)

            if request.data.get('content'):
                post_obj.content = request.data.get('content')

            if request.data.get('image_url'):
                post_obj.content = request.data.get('content')
            
            post_obj.save()

        except WorkSpaceModel.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid post"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "post updated"
        }, status=status.HTTP_200_OK)

    def delete(self, request):

        try:
            post_obj = Post.objects.get(pk=request.data.get('post_id'), user=request.user)
            post_obj.delete()

        except WorkSpaceModel.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid post"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "post deleted"
        }, status=status.HTTP_200_OK)

class CommentView(PrivateAPI):

    def put(self, request):
        
        workspace_obj = validate_user_and_workspace(request)

        if isinstance(workspace_obj, Response):
            return workspace_obj

        try:
            post_obj = Post.objects.get(
                pk = request.data.get('post_id'),
                workspace__id = request.data.get('workspace_id')
            )
        except Post.DoesNotExist:
            return Response({
            "status": False,
            "message": "post not found"
        }, status=status.HTTP_400_BAD_REQUEST)


        comment = {
            'user': request.user,
            'post': post_obj,
            'content': request.data.get('content')
        }

        comment_obj = Comment.objects.create(**comment)

        return Response({
            "status": True,
            "message": "comment created",
            "post_id": comment_obj.id
        }, status=status.HTTP_200_OK)

    def post(self, request):

        try:
            commnet_obj = Comment.objects.get(
                pk = request.data.get('comment_id'),
                user = request.user
            )
            if request.data.get('content'):
                commnet_obj.content = request.data.get('content')
                commnet_obj.save()

        except Comment.DoesNotExist:
            return Response({
                "status": False,
                "message": "comment not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "comment updated"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            commnet_obj = Comment.objects.get(
                pk = request.data.get('comment_id'),
                user = request.user
            )
            commnet_obj.delete()
        except Comment.DoesNotExist:
            return Response({
                "status": False,
                "message": "comment not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "comment updated"
        }, status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 25
        
class AllPosts(PrivateListAPI):
    
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):

        workspace_id = request.GET.get('workspace_id')
        self.queryset = self.queryset.filter(workspace__id=workspace_id)

        return super().get(request, *args, **kwargs)

class AllComments(PrivateListAPI):
    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):

        post_id = request.GET.get('post_id')
        self.queryset = self.queryset.filter(post__id=post_id)

        return super().get(request, *args, **kwargs)

class LinkeView(PrivateAPI):

    def post(self, request):

        workspace_obj = validate_user_and_workspace(request)

        if isinstance(workspace_obj, Response):
            return workspace_obj

        try:
            post_obj = Post.objects.get(
                pk = request.data.get('post_id'),
                workspace__id = request.data.get('workspace_id')
            )
        except Post.DoesNotExist:
            return Response({
                "status": False,
                "message": "post not found"
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            like = Like.objects.create(user=request.user, post=post_obj)
        except Exception as e:
            return Response({
                "status": False,
                "message": "Already liked"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": True,
            "message": "post liked",
            "liked_by": like.user.username
        }, status=status.HTTP_200_OK)


