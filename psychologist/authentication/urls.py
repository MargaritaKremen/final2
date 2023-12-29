from django.urls import path
from .views import register, auth, logout_page

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/', auth, name='auth'),
    path('logout/', logout_page, name='logout'),
]