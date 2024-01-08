from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib import messages # для профілей
import logging

logger = logging.getLogger(__name__)

def profiles(request):
    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        avatar = request.FILES.get('avatar')
        date_of_birth = request.POST.get('date_of_birth')        

        # чи вже є профіль для користувача:
        try:
            profile, created  = UserProfile.objects.get_or_create(user=user)
            profile.date_of_birth = date_of_birth
            profile.avatar = avatar
            profile.full_name = full_name
            profile.save()
            messages.success(request, 'Профіль успішно оновлено.')
            return redirect('profiles')
        except Exception as e:
            logger.error(f"Error in profiles view: {e}", exc_info=True)
            messages.error(request, f'Помилка: {e}')

        return redirect('profiles') 
    else:
    # Якщо метод запиту GET, просто відображати сторінку з профілями
        profiles = UserProfile.objects.all()
        return render(request, 'profiles/profiles.html', {'profiles': profiles})
