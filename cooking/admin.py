from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_published', 'watched', 'created_at')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    readonly_fields = ('watched',)
    list_filter = ('is_published', 'category',)
    ordering = ('-created_at',)


