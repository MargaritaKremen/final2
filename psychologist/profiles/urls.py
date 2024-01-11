from django.conf.urls.static import static
from psychologist.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.urls import path
from .views import profiles, edit_profile, view_profile, create_profile

urlpatterns = [
    path('profiles/', profiles, name='profiles'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/create/', create_profile, name='create_profile'),
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)