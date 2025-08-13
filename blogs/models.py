from django.db import models
import os
from django.conf import settings
from accounts.models import User

# Create your models here.
class Blog(models.Model):

    title_image = models.FileField(upload_to="title_images/")
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=False)
    rating = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user_name}"
    
    # def delete(self, *args, **kwargs):
    #     """
    #     Ensure that all related comments and likes are deleted first
    #     before deleting the blog itself.
    #     """
    #     self.comments.all().delete()
    #     self.likes.all().delete()
    #     super().delete(*args, **kwargs)




class Comment(models.Model):

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    blog_name = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} on {self.blog_name}"
    



class Like(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    blog_name = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_name', 'blog_name')

    def __str__(self):
        return f"{self.user_name} liked {self.blog_name.title}"