from django.contrib import admin
from .models import Post, Comment, Like, Category, UserProfile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'date_of_birth', 'get_favorite_articles')

    def get_favorite_articles(self, obj):
        return ", ".join([str(article) for article in obj.favorite_articles.all()])

    get_favorite_articles.short_description = 'Favorite Articles'

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Like, LikeAdmin)