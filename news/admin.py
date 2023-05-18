from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'categoryType', 'dateCreation', 'rating', 'is_published')
    list_display_links = ('id', 'title')
    list_filter = ('dateCreation', 'categoryType', 'rating')
    search_fields = ('title', 'text')
    list_editable = ('is_published',)

class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'authorUser', 'ratingAuthor',)
    list_display_links = ('id', 'authorUser')
    list_filter = ('ratingAuthor', 'authorUser')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('subscribers', 'name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentPost', 'commentUser', 'dateCreation', 'rating')
    list_display_links = ('id', 'commentPost')
    list_filter = ('dateCreation', 'rating', 'commentUser')

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'postThrough', 'categoryThrough')
    list_display_links = ('id', 'postThrough')
    list_filter = ('categoryThrough',)


# Register your models here.
admin.site.register(Author, AutorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)

