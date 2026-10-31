from django.db import models
from django.urls import reverse


class Category(models.Model):
    '''Категория новостей'''
    title = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self): # чтоб писать {{ category.get_absolute_url }} вместо url
        return reverse('cooking:category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Post(models.Model):
    '''Для новостных постов'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts',
                                 verbose_name="Категория статьи")

    title = models.CharField(max_length=100, verbose_name='Название статьи')
    content = models.TextField(default='Скоро здесь будет статья', verbose_name="Содержимое статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True, verbose_name="Фото")
    watched = models.IntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано(Да/Нет)")  # опубликовано по умолчанию

    def __str__(self):
        return f'{self.category} | {self.title} | {self.created_at:%d.%m.%Y}'

    def get_absolute_url(self): # чтоб писать {{ post.get_absolute_url }} вместо url
        return reverse('cooking:post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
