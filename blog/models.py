from django.db import models
from django.conf import settings
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='author')

class Comment(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    post = models.ForeignKey(Post,on_delete=models.PROTECT,related_name='comment')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)