from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib import messages # для профілей
import logging
from django.contrib.auth.decorators import login_required
from django.http import Http404

logger = logging.getLogger(__name__)

@login_required
def view_profile(request):
    
    try:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'profiles/view_profile.html', {'profile': profile})
    except UserProfile.DoesNotExist:
        messages.error(request, 'Профіль не знайдено. Створіть профіль, щоб переглянути.')
        return redirect('profiles') 

def edit_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        avatar = request.FILES.get('avatar')
        date_of_birth = request.POST.get('date_of_birth')

        if profile:
            profile.full_name = full_name
            profile.avatar = avatar
            profile.date_of_birth = date_of_birth
            profile.save()
            messages.success(request, 'Профіль успішно оновлено.')
        else:
            UserProfile.objects.create(user=request.user, full_name=full_name, avatar=avatar, date_of_birth=date_of_birth)
            messages.success(request, 'Профіль успішно створено.')

        return redirect('view_profile')

    return render(request, 'profiles/edit_profile.html', {'profile': profile})

def create_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        avatar = request.FILES.get('avatar')
        date_of_birth = request.POST.get('date_of_birth')

        if profile:
            profile.full_name = full_name
            profile.avatar = avatar
            profile.date_of_birth = date_of_birth
            profile.save()
            messages.success(request, 'Профіль успішно оновлено.')
        else:
            UserProfile.objects.create(user=request.user, full_name=full_name, avatar=avatar, date_of_birth=date_of_birth)
            messages.success(request, 'Профіль успішно створено.')

        return redirect('view_profile')

    return render(request, 'profiles/create_profile.html', {'profile': profile})


# це створення профіля
def profiles(request):
    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        avatar = request.FILES.get('avatar')
        date_of_birth = request.POST.get('date_of_birth')

        # чи вже є профіль для користувача:
        try:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.date_of_birth = date_of_birth
            profile.avatar = avatar
            profile.full_name = full_name
            profile.save()
            messages.success(request, 'Профіль успішно оновлено.')
            return redirect('view_profile')
        except Exception as e:
            logger.error(f"Error in profiles view: {e}", exc_info=True)
            messages.error(request, f'Помилка: {e}')

        return redirect('profiles') 
    else:
        # Якщо метод запиту GET, просто відображати сторінку з профілями
        profiles = UserProfile.objects.all()
        return render(request, 'profiles/profiles.html', {'profiles': profiles})
