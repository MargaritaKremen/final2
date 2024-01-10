from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile

def main(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def works(request):
    return render(request, 'main/works.html')

def blog(request):
    return render(request, 'main/blog.html')







