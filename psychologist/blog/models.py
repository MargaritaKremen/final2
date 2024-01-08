from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name    

class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

class Like(models.Model):
    article = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name='user_favorited_articles', blank=True)
    image = models.ManyToManyField(PostImage, related_name='post_images', blank=True)
    liked_users = models.ManyToManyField(User, through='Like', related_name='user_likes', blank=True)    
    # profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
