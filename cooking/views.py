from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Category, Post
from django.db.models import F
from .forms import PostForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView


# def index(request, pk=None):
#     '''Для главной страницы с выбором по категориям'''
#     categories = Category.objects.all()
#
#     if pk:  # Если pk передан (кликнули на категорию)
#         category = get_object_or_404(Category, id=pk) # Безопасно ищем категорию
#         posts = Post.objects.filter(category=category)
#         title = category.title # Берем название категории
#     else:
#         posts = Post.objects.all()
#         title = 'Кулинарный сайт'
#
#     context = {
#         'title': title,
#         'posts': posts,
#         'categories': categories,
#         'active_category': pk,  # <-- Передаем ID активной категории (или None, если главная)
#     }
#     return render(request, 'cooking/index.html', context)

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


# def post_detail(request, pk):
#     '''Детальный показ поста'''
#     post = get_object_or_404(Post, pk=pk)
#     Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
#     related_posts = Post.objects.exclude(pk=post.pk).order_by('?')[:3] # 3 random поста из этой же категории
#     # related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:3]
#
#     context = {
#         'post': post,
#         'related_posts': related_posts,
#     }
#
#     return render(request, 'cooking/post_detail.html', context)


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
        return context


# def add_post(request):
#     '''Добавление статьи от пользователя без админки'''
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = Post.objects.create(**form.cleaned_data)
#             # post.save() # не нужно - дублирует первый способ, лучше сразу писать post.save() - аналогично ↑
#             messages.success(request, 'Вы успешно создали новый рецепт!')
#             return redirect('cooking:post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#
#     context = {
#         'form': form,
#         'title': 'Добавить рецепт'
#     }
#
#     return render(request, 'cooking/add_post.html', context)

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
