from django.urls import reverse
from itertools import groupby
from operator import itemgetter
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseNotFound
from .models import Like, Post, PostImage, Category
# from .forms import PostForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from os.path import join #для FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment
import logging

logger = logging.getLogger(__name__)



def article_list(request):
    posts_by_category = {
        category: list(posts)
        for category, posts in groupby(Post.objects.all(), key=lambda post: post.category)
    }

    context = {'posts_by_category': posts_by_category}
    return render(request, 'blog/article_list copy 2.html', context)



# def article_detail(request, article_id):
#     post = get_object_or_404(Post, pk=article_id)
#     all_categories = Category.objects.all()
#     current_category = post.category

#     context = {'post': post, 'all_categories': all_categories, 'current_category': current_category}
#     return render(request, 'blog/article_detail.html', context)


@login_required(login_url='/authentication/auth/')
def article_detail(request, article_id):
    try:
        post = get_object_or_404(Post, pk=article_id)
        user = request.user
        all_categories = Category.objects.all()
        current_category = post.category
        liked = Like.objects.filter(article=post, user=user).exists()

        context = {
            'post': post,
            'liked': liked,
            'all_categories': all_categories, 
            'current_category': current_category,
        }

        return render(request, 'blog/article_detail.html', context)
    except Exception as e:
        print(f"Error in article_detail: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    print(f"Category ID: {category_id}")
    print(f"Selected Category: {category.name}")    
    posts = Post.objects.filter(category=category).order_by('-created_at')
    print(f"Filtered Posts: {posts}")

    
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {'posts': posts, 'category': category}
    return render(request, 'blog/category_posts.html', context)


# @login_required(login_url='/authentication/auth/')
def add_to_favorites(request, article_id):
    post = get_object_or_404(Post, pk=article_id)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('article_detail', article_id=article_id)


# @login_required(login_url='/authentication/auth/')
def like_article(request, article_id):
    try:
        post = get_object_or_404(Post, pk=article_id)
        user = request.user

        # Проверка, лайкнул ли пользователь уже статью
        like, created = Like.objects.get_or_create(article=post, user=user)

        liked = False
        if not created:
            like.delete()
        else:
            liked = True

        # Обновление поля liked_users в модели Post
        post.liked_users.add(user) if liked else post.liked_users.remove(user)
        
        # Отправка JSON-ответа с информацией о лайках и состоянии
        data = {
            'liked': liked,
            'likes_count': post.like_set.count(),  
        }

        return JsonResponse(data)
    except Exception as e:
        # Логирование ошибки
        logger.error(f"Error in like_article: {e}", exc_info=True)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


    

@require_POST
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    content = request.POST.get('content', '')
    
    if content:
        comment = Comment.objects.create(article=post, author=request.user, content=content)
        return JsonResponse({'success': True, 'comment': {'author': comment.author.username, 'content': comment.content}})
    else:
        return JsonResponse({'success': False, 'error': 'Content is required'})


def add_post(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        post = Post.objects.create(title=title, author=author, content=content, category=category)

        # Создаем список для хранения созданных объектов PostImage
        post_images = []

        for upload in request.FILES.getlist('images'):
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)

            # Создаем объект PostImage, связываем с постом, и добавляем в список
            post_image = PostImage.objects.create(post=post, image=file_url)
            post_images.append(post_image)

        # Используем метод set для установки всех объектов PostImage для данного поста
        post.image.set(post_images)

        return redirect('article_list')

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'blog/add_post.html', context)