from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Категорія')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name    

class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', verbose_name='Зображення')    

class Like(models.Model):
    article = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Стаття')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes', verbose_name='Користувач')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'    

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Зміст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категорія')
    favorites = models.ManyToManyField(User, related_name='user_favorited_articles', blank=True, verbose_name='Улюблені статті')
    image = models.ManyToManyField(PostImage, related_name='post_images', blank=True, verbose_name='Зображення')
    liked_users = models.ManyToManyField(User, through='Like', related_name='user_likes', blank=True, verbose_name='Користувачі, що поставили лайк')  
      
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости' 
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', verbose_name='Стаття')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Зміст коментаря')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі' 

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
