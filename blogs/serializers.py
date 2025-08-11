
from rest_framework import serializers
from .models import Blog, Like, Comment
from accounts.models import User, UserManager, BaseUserManager, AbstractBaseUser

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id", "title_image", "title", "slug", "description", "rating", "created_at"
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user_name'] = request.user
        return super().create(validated_data)
    


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'comment_text', 'blog_name', 'created_at', 'updated_at']



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id', 'user_name', 'blog_name', 'created_at'
        ]