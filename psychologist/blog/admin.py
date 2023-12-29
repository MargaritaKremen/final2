from django.contrib import admin
from .models import Post, Comment, Like, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category, CategoryAdmin)