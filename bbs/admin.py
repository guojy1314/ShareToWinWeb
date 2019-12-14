from django.contrib import admin
from .models import Article, ArticleTopic, ArticleComment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time')


class ArticleTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTopic, ArticleTopicAdmin)
