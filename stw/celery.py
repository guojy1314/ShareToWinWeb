from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stw.settings')  # 设置django环境
# 实例化Celery
app = Celery('stw')
# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings')
# Celery加载所有注册应用中的tasks.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)