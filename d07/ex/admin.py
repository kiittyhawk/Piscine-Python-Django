from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

class FavouriteArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')
    search_fields = ('user',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(UserFavouriteArticle, FavouriteArticleAdmin)