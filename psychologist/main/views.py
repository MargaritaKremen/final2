from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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

def profiles(request):
    return render(request, 'blog/profiles.html')




