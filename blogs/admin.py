from django.contrib import admin
from .models import Blog, Comment, Like




@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'title_image', 'slug', 'description', 'user_name', 'rating', 'created_at', 'updated_at']
    search_fields = ['title', 'slug', 'description', 'user_name']
    list_filter = ['created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'comment_text', 'blog_name', 'created_at', 'updated_at']



@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    list_display= ['id', 'user_name', 'blog_name', 'created_at']