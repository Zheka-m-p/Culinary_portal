from django.urls import path
from . import views

app_name='cooking'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.index, name='category_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    # добавляем формы
    path('posts/add_post/', views.add_post, name='add_post'),

]