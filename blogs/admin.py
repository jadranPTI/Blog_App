from django.contrib import admin
from .models import Blog, Comment, Like

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'title_image', 'slug', 'description',
        'user_name', 'rating', 'created_at', 'updated_at'
    ]
    # search_fields = ['title', 'slug', 'description', 'user_name']
    # list_filter = ['created_at']
    # ordering = ['-created_at']
    # date_hierarchy = 'created_at'

    # def delete_queryset(self, request, queryset):
    #     """
    #     Custom bulk delete to ensure related comments and likes
    #     are removed before deleting the blog.
    #     """
    #     for blog in queryset:
    #         Comment.objects.filter(blog_name=blog).delete()
    #         Like.objects.filter(blog_name=blog).delete()
    #         blog.delete()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'comment_text', 'blog_name', 'created_at', 'updated_at']

@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'blog_name', 'created_at']











# from django.contrib import admin
# from .models import Blog, Comment, Like




# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'title_image', 'slug', 'description', 'user_name', 'rating', 'created_at', 'updated_at']
#     search_fields = ['title', 'slug', 'description', 'user_name']
#     list_filter = ['created_at']
#     ordering = ['-created_at']
#     date_hierarchy = 'created_at'

#     # def delete_queryset(self, request, queryset):
#     #     # Delete related comments and likes first
#     #     Comment.objects.filter(blog_name__in=queryset).delete()
#     #     Like.objects.filter(blog_name__in=queryset).delete()
#     #     # Now delete blogs
#     #     super().delete_queryset(request, queryset)
#     def delete_queryset(self, request, queryset):
#         """
#         Custom bulk delete to make sure related objects are removed first.
#         """
#         for blog in queryset:
#             blog.delete()  # This calls our overridden delete() method


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user_name', 'comment_text', 'blog_name', 'created_at', 'updated_at']



# @admin.register(Like)
# class LikesAdmin(admin.ModelAdmin):
#     list_display= ['id', 'user_name', 'blog_name', 'created_at']