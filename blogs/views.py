
from django.shortcuts import render
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication
from rest_framework import generics
from .serializers import BlogSerializer, LikeSerializer, CommentSerializer
from accounts.models import User
from .models import Blog, Comment, Like
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class BlogCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            search_query = request.query_params.get('search', None)

            queryset = Blog.objects.all()
            paginator = CustomPageNumberPagination()

            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(slug__icontains=search_query)
                ).distinct()

            page = paginator.paginate_queryset(queryset, request)
            serializer = BlogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            # logging.error(f"Blogs list not found: {str(e)}", exc_info=True)
            return Response({'message': 'Blogs list not found'}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            serializer = BlogSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user_name=request.user)
            return Response(
                {
                    'message': 'Blog created successfully'
                }, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # logging.error(f"Blog creation failed: {str(e)}", exc_info=True)
            return Response({"message": "Blog creation failed. Please check the provided data"}, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            blogs = get_object_or_404(Blog, pk=pk)
            serializer = BlogSerializer(blogs)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Blog.objects.get(pk=pk)
        except Exception as e:
            # logging.error(f"Blog not found: {str(e)}", exc_info=True)
            return Response({"message": "Blog not found"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request, pk):
        try:
            blog = get_object_or_404(Blog, pk=pk)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # logging.error(f"Blog not found: {str(e)}", exc_info=True)
            return Response({"message": "Blog not found"}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk, user_name=request.user)
            blog.delete()
            return Response({"message": "Blog deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            # logging.error(f"Blogs not found: {str(e)}", exc_info=True)
            return Response({"message": "Blog not found"}, status=status.HTTP_400_BAD_REQUEST)




class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            blog_name = request.query_params.get('blog_id')

            if not blog_name:
                return Response(
                    {"message": "blog_id query parameter is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Filter comments by blog_id
            comments = Comment.objects.filter(blog_name=blog_name).order_by('-created_at')

            if not comments.exists():
                return Response(
                    {"message": "No comments found for this blog."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': 'Comments not found'}, status=status.HTTP_400_BAD_REQUEST)




    def post(self, request):
        try:
            blog_id = request.data.get('blog_id')
            comment_text = request.data.get('content')

            if not blog_id or not comment_text:
                return Response({
                    "message": "Both 'blog_id' and 'content' are required."
                }, status=status.HTTP_400_BAD_REQUEST)
        
            blog_name = get_object_or_404(Blog, id=blog_id)
            comment_text = Comment.objects.create(
                blog_name=blog_name,
                user_name=request.user,
                comment_text=comment_text
            )

            return Response(CommentSerializer(comment_text).data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'message': "Sorry! You can't comment on this blog"}, status=status.HTTP_400_BAD_REQUEST)




class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            blog_name = request.query_params.get('blog_id')

            if not blog_name:
                return Response({
                    'message': "blog_id query parameter is required."
                })
        
            likes = Like.objects.filter(blog_name=blog_name)
            if not likes:
                return Response({
                    "message": "No likes found for this blog."
                })
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': "No likes found of this blog"}, status=status.HTTP_400_BAD_REQUEST)




    def post(self, request):
        try:
            blog_id = request.data.get("blog_id")

            if not blog_id:
                return Response({"message": "blog_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            blog = get_object_or_404(Blog, id=blog_id)

            existing_like = Like.objects.filter(user_name=request.user, blog_name=blog).first()

            if existing_like:
            # If like exists, remove it (dislike)
                existing_like.delete()
                return Response({"message": "Blog unliked successfully"}, status=status.HTTP_200_OK)

        # Otherwise, create a new like
            Like.objects.create(user_name=request.user, blog_name=blog)
            return Response({"message": "Blog liked successfully"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'message': "You can't like of this blog"}, status=status.HTTP_400_BAD_REQUEST)
    

class CustomPageNumberPagination(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=100