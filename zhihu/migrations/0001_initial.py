# Generated by Django 2.0.3 on 2019-12-11 00:20

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import zhihu.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='回答内容')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('voteup_nums', models.IntegerField(default=0, verbose_name='认同数')),
                ('votedown_nums', models.IntegerField(default=0, verbose_name='不认同数')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='匿名回答')),
                ('author', models.ForeignKey(on_delete=models.SET(zhihu.models.get_sentinel_user), to=settings.AUTH_USER_MODEL, verbose_name='回答作者')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300, verbose_name='评论')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zhihu.Answer', verbose_name='回答')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='问题标题')),
                ('content', models.TextField(blank=True, null=True, verbose_name='问题内容')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('recommend', models.BooleanField(default=False, verbose_name='是否推荐')),
                ('read_nums', models.IntegerField(default=0, verbose_name='浏览量')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='匿名问题')),
                ('author', models.ForeignKey(on_delete=models.SET(zhihu.models.get_sentinel_user), to=settings.AUTH_USER_MODEL, verbose_name='问题作者')),
            ],
            options={
                'ordering': ['-pub_time'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='话题')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='话题描述')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('image', models.ImageField(blank=True, default='image/default_topic.jpg', null=True, upload_to='image/%Y/%m/', verbose_name='话题图片')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='用户话题')),
            ],
        ),
        migrations.CreateModel(
            name='UserCollectAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zhihu.Answer', verbose_name='回答')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zhihu.Answer', verbose_name='回答')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zhihu.Question', verbose_name='问题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(blank=True, to='zhihu.Topic', verbose_name='话题'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=models.SET(zhihu.models.get_sentinel_question), to='zhihu.Question', verbose_name='回答问题'),
        ),
    ]
