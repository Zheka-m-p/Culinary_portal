from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.db.models import F

def index(request, pk=None):
    '''Для главной страницы с выбором по категориям'''
    categories = Category.objects.all()

    if pk:  # Если pk передан (кликнули на категорию)
        category = get_object_or_404(Category, id=pk) # Безопасно ищем категорию
        posts = Post.objects.filter(category=category)
        title = category.title # Берем название категории
    else:
        posts = Post.objects.all()
        title = 'Кулинарный сайт'

    context = {
        'title': title,
        'posts': posts,
        'categories': categories,
        'active_category': pk,  # <-- Передаем ID активной категории (или None, если главная)
    }
    return render(request, 'cooking/index.html', context)


def post_detail(request, pk):
    '''Детальный показ поста'''
    post = get_object_or_404(Post, pk=pk)
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    related_posts = Post.objects.exclude(pk=post.pk).order_by('?')[:3] # 3 random поста из этой же категории
    # related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }

    return render(request, 'cooking/post_detail.html', context)