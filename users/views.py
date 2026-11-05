from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from cooking.models import Post



def user_login(request):
    '''Аутентификация пользователя (вход по логину и паролю)'''
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # AuthenticationForm уже проверила пароль. Просто берем юзера.
            user = form.get_user()
            login(request, user)  # Создаем сессию
            messages.success(request, message='Вы успешно вошли в аккаунт')
            return redirect('cooking:index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }
    # Исправлено: путь к шаблону в приложении users
    return render(request, 'users/login.html', context)


def user_logout(request):
    '''Выход пользователя'''
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')  # <-- Добавили
    return redirect('cooking:index')


def user_register(request):
    '''Регистрация пользователя'''
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь можете войти в систему.')
            return redirect('users:login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': 'Регистрация пользователя'}

    return render(request, 'users/register.html', context)


def user_profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user_profile).order_by('-created_at')
    context = {
        'user_profile': user_profile,
        'posts': posts,
    }

    return render(request, 'users/profile.html', context)