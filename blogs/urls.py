from django.urls import path
from .views import BlogCreateAPIView, BlogDetailAPIView, CommentAPIView, LikeAPIView

urlpatterns = [
    path("blogs", BlogCreateAPIView.as_view(), name="list_create_blogs"),
    path("blogs/<int:pk>", BlogDetailAPIView.as_view(), name= "retrieve_update_delete_blog"),
    path('comment', CommentAPIView.as_view(), name = 'comments'),
    path('blog/like', LikeAPIView.as_view(), name='like'),
]