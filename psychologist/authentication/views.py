from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError


def register(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            context['username'] = username
            context['email'] = email
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if username:
                if email:
                    if '@' in email:
                        if password:
                            if password == confirm_password:
                                if len(password) >= 8:
                                    # pass
                                    try:
                                        User.objects.create_user(username=username, email=email, password=password)
                                        return redirect('auth')
                                    except IntegrityError:
                                        context['error'] = 'Такий користувач вже існує'
                                else:
                                    context['error'] = 'Довжина паролю має бути більше 8 символів'
                            else:
                                context['error'] = 'Паролі не співпадають'
                        else:
                            context['error'] = 'Заповніть всі поля'
                    else:
                        context['error'] = 'Введіть коректну електронну пошту'
                else:
                    context['error'] = 'Заповніть всі поля'
            else:
                context['error'] = 'Заповніть всі поля'

        return render(request, 'authentication/register.html', context)
    else:
        return redirect('main')


def auth(request):
    print("Auth view called.")
    if not request.user.is_authenticated:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            context['username'] = username
            password = request.POST.get('password')
            print(password, username)
            if username and password:
                user = authenticate(username=username, password=password)
                print(user)
                if user:
                    login(request, user)
                    return redirect('main')
                else:
                    context['error'] = 'Логін або пароль невірні'
            else:
                context['error'] = 'Заповніть всі поля'
        return render(request, 'authentication/auth.html', context)
    else:
        return redirect('main')


def main(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/auth_main.html')
    else:
        return redirect('auth')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('auth')