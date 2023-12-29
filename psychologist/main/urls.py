from django.urls import path
from .views import main, about, contact, works, blog
from authentication.views import auth
from blog.views import article_list


urlpatterns = [
    path('', main, name='main'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('works/', works, name='works'),
    path('blog/', blog, name='blog'),
    path('authentication/auth/', auth, name='auth'),
    path('blog/articles/', article_list, name='article_list'),
]