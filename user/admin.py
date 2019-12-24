from django.contrib import admin

from .models import User, CheckCode, UserRelationship


admin.site.site_header = '分享为赢后台管理'
admin.site.site_title = '登录后台管理'
admin.site.index_title = '后台管理'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'email')


class CheckCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_code', 'add_time')


class UserRelationshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'add_time')


admin.site.register(User, UserAdmin)
admin.site.register(CheckCode, CheckCodeAdmin)
admin.site.register(UserRelationship, UserRelationshipAdmin)
