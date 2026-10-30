from django.db import models


class Category(models.Model):
    '''Категория новостей'''
    title = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(models.Model):
    '''Для новостных постов'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория статьи")

    title = models.CharField(max_length=100, verbose_name='Название статьи')
    content = models.TextField(default='Скоро здесь будет статья', verbose_name="Содержимое статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True, verbose_name="Фото")
    watched = models.IntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано(Да/Нет)") # опубликовано по умолчанию

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.category} | {self.title} | {self.created_at}'
