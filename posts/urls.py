from django.urls import path
from .views import PostView, CommentView, AllPosts, AllComments, LinkeView, GetPost

urlpatterns = [
    path('post/', PostView.as_view()),
    path('get/post/', GetPost.as_view()),
    path('comment/', CommentView.as_view()),
    path('view/posts/', AllPosts.as_view()),
    path('view/comments/', AllComments.as_view()),
    path('like/post/', LinkeView.as_view()),
]