from django.contrib import admin
from .models import Article, ArticleTopic, Comment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_time')


class ArticleTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_time')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'get_comment', 'created')

    def get_comment(self,obj):
        return obj.content[:50]

    get_comment.short_description = '回帖内容'


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTopic, ArticleTopicAdmin)
admin.site.register(Comment, CommentAdmin)
