from django.urls import path
from .views import article_list, article_detail, add_to_favorites,  add_post, like_article,category_posts, add_comment

app_name = 'blog'

urlpatterns = [
    # path('profiles/', profiles, name='profiles'),
    path('article_list/', article_list, name='article_list'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('category/<int:category_id>/', category_posts, name='category_posts'),
    path('article/<int:article_id>/add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('add_post/', add_post, name='add_post'), 
    path('article/<int:article_id>/like/', like_article, name='like_article'),    
    path('<int:post_id>/add_comment/', add_comment, name='add_comment'),
]