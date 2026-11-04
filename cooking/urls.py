from django.urls import path
from . import views

app_name='cooking'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('category/<int:pk>/', views.index, name='category_list'),
    # path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    # добавляем формы
    # path('posts/add_post/', views.add_post, name='add_post'),
    # переходим на классы
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:pk>/', views.IndexView.as_view(), name='category_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/add_post/', views.PostCreateView.as_view(), name='add_post'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),

]