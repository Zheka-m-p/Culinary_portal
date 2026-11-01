from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    '''Форма для добавлений новой статьи от пользователя'''

    class Meta:
        '''Класс указывающий поведенческий характер - чертеж для класса'''
        model = Post # просто объект этого класса (пост)
        fields = ('title', 'category', 'photo', 'content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


