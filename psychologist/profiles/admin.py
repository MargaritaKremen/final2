from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'date_of_birth', 'get_favorite_articles')

    def get_favorite_articles(self, obj):
        return ", ".join([str(article) for article in obj.favorite_articles.all()])

    get_favorite_articles.short_description = 'Favorite Articles'

admin.site.register(UserProfile, UserProfileAdmin)