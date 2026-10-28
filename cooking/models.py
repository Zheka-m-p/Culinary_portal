from django.db import models


class Category(models.Model):
    '''Категория новостей'''
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(models.Model):
    '''Для новостных постов'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(default='Скоро здесь будет статья')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    watched = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True) # опубликовано по умолчанию

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.title} | {self.created_at}'
