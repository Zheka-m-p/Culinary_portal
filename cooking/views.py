from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Category, Post, Comment
from django.db.models import F, Q
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView


class IndexView(ListView):
    '''Класс для отображения главной страницы и страницы категорий'''
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'

    def get_queryset(self):
        '''Для доп. фильтрации данных (по умолачиню все записи идут через классы)'''
        pk = self.kwargs.get('pk')  # Получаем pk из URL (если мы на странице категории)

        if pk:  # Если pk есть, фильтруем посты по категории
            self.category = get_object_or_404(Category, id=pk)
            return Post.objects.filter(category=self.category, is_published=True).order_by('-watched')

        return Post.objects.filter(is_published=True)  # Если pk нет (главная страница), отдаем все опубликованные посты

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем базовый контекст (в нем уже есть 'posts')
        # Ниже добавляем категории, в которых есть опубликованные посты(нужны для меню слева)
        context['categories'] = Category.objects.filter(posts__is_published=True).distinct()

        pk = self.kwargs.get('pk')  # Передаем active_category, чтобы работала подсветка синим
        context['active_category'] = pk

        if pk:  # Формируем заголовок страницы
            context['title'] = self.category.title
        else:
            context['title'] = 'Кулинарный сайт'

        return context


class SearchView(IndexView):
    '''Поиск по постам (наследуется от IndexView)'''

    def get_queryset(self):
        qs = super().get_queryset()  # Берем базовый queryset из IndexView
        word = self.request.GET.get('q')  # Получаем слово из формы

        if word:
            # Ищем по названию ИЛИ по содержимому
            qs = qs.filter(Q(title__icontains=word) | Q(content__icontains=word))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = self.request.GET.get('q')
        if word:
            context['title'] = f'Результаты поиска: «{word}»'
        else:
            context['title'] = 'Поиск по рецептам'
        return context


class PostDetailView(DetailView):
    '''Страница поста(статьи-рецепта)'''
    model = Post
    context_object_name = 'post'
    template_name = 'cooking/post_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(watched=F('watched') + 1)
        obj.watched += 1  # Синхронизируем объект в памяти для отображения в шаблоне
        # obj.refresh_from_db()  # 2 вариант: ОБНОВИТЬ В БД СРАЗУ ЖЕ
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.exclude(pk=self.kwargs.get('pk')).order_by('?')[:3]
        context['comment_form'] = CommentForm()  # форма для коммента добавлена в словарь

        return context


class PostCreateView(CreateView):
    '''Создание поста через классы'''
    model = Post
    form_class = PostForm
    extra_context = {'title': 'Добавить статью'}
    success_url = reverse_lazy('cooking:index')
    template_name = 'cooking/add_post.html'


class PostUpdateView(UpdateView):
    '''Для редактирования статьи'''
    model = Post
    form_class = PostForm
    context_object_name = 'post'
    template_name = 'cooking/update_post.html'
    # редирект после направления уже есть (метод get_absolute_url() в модели Post)


class PostDeleteView(DeleteView):
    '''Для удаления поста'''
    model = Post
    context_object_name = 'post'
    template_name = 'cooking/delete_post.html'
    success_url = reverse_lazy('cooking:index')
    # form_class = PostForm # он тут не нужен для удаления поста


class CommentCreateView(LoginRequiredMixin, CreateView):
    '''Форма для создания комментария к посту '''
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        ''' Находим пост по pk из URL и привязываем автора '''
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        '''Возвращаем URL поста + якорь #comments'''
        return self.object.get_absolute_url() + '#comments'
