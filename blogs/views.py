
from django.shortcuts import render
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication
from rest_framework import generics
from .serializers import BlogSerializer, LikeSerializer, CommentSerializer
from accounts.models import User, UserManager, BaseUserManager, AbstractBaseUser
from .models import Blog, Comment, Like
from django.shortcuts import get_object_or_404
from django.db.models import Q

class BlogCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', None)

        queryset = Blog.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(slug__icontains=search_query)
            ).distinct()

        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            logging.error(f"Blog creation failed: {str(e)}", exc_info=True)
            return Response({"error": "Blog creation failed. Please check the provided data"}, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailAPIView(APIView):

    def get(self, pk):
        try:
            blogs = get_object_or_404(Blog, pk=pk)
            serializer = BlogSerializer(blogs)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Blog.objects.get(pk=pk)
        except Exception as e:
            logging.error(f"Blog not found: {str(e)}", exc_info=True)
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request, pk):
        try:
            blog = get_object_or_404(Blog, pk=pk)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Blogs not found: {str(e)}", exc_info=True)
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk, user_name=request.user)
            blog.delete()
            return Response({"message": "Blog deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            logging.error(f"Blogs not found: {str(e)}", exc_info=True)
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)




class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get blog_id from query parameters
        blog_name = request.query_params.get('blog_id')

        if not blog_name:
            return Response(
                {"error": "blog_id query parameter is required."},
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




    def post(self, request):
        blog_id = request.data.get('blog_id')
        comment_text = request.data.get('content')

        if not blog_id or not comment_text:
            return Response({
                "error": "Both 'blog_id' and 'content' are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        blog_name = get_object_or_404(Blog, id=blog_id)
        comment_text = Comment.objects.create(
            blog_name=blog_name,
            user_name=request.user,
            comment_text=comment_text
        )

        return Response(CommentSerializer(comment_text).data, status=status.HTTP_201_CREATED)




class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        blog_id = request.data.get("blog_id")

        if not blog_id:
            return Response({"error": "blog_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        blog = get_object_or_404(Blog, id=blog_id)

        existing_like = Like.objects.filter(user_name=request.user, blog_name=blog).first()

        if existing_like:
            # If like exists, remove it (dislike)
            existing_like.delete()
            return Response({"message": "Blog unliked successfully"}, status=status.HTTP_200_OK)

        # Otherwise, create a new like
        Like.objects.create(user_name=request.user, blog_name=blog)
        return Response({"message": "Blog liked successfully"}, status=status.HTTP_201_CREATED)