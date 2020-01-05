from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class ArticleTopic(models.Model):
    '''文章话题分类'''
    name = models.CharField('文章话题', max_length=40)
    description = models.CharField('话题描述', max_length=200, null=True,
                                   blank=True)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    # image = models.ImageField('话题图片', upload_to='image/%Y/%m/',
    #                           default='image/default_topic.jpg', null=True,
    #                           blank=True)
    #
    # users = models.ManyToManyField(User, blank=True, verbose_name='用户话题')

    def __str__(self):
        return self.name

    # def get_user_nums(self):
    #     #     '''获取关注者数量'''
    #     #     return self.users.count()

    def get_article_nums(self):
        '''获取文章话题的发帖数'''
        return self.article_set.count()


class Article(models.Model):
    '''文章帖子模型'''
    title = models.CharField('文章标题', max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user),
                               verbose_name='文章作者')
    content = RichTextUploadingField('文章内容', null=True, blank=True)
    topics = models.ManyToManyField(ArticleTopic, blank=True, verbose_name='文章话题')
    pub_time = models.DateTimeField('发布时间', auto_now_add=True)
    recommend = models.BooleanField('是否推荐', default=False)
    read_nums = models.IntegerField('浏览量', default=0)
    is_anonymous = models.BooleanField('匿名问题', default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']

    # def get_comment_nums(self):
    #     '''获取回帖评论数量'''
    #     return self.parents.count()

    # def get_follow_est_comment(self):
    #     '''获取点赞最多的回答'''
    #     return self.comment_set.annotate(
    #         follow_nums=models.Count('userfollowcomment')).order_by(
    #         '-follow_nums').first()

    def get_topic_name(self):
        '''获取文章话题名'''
        return self.topics.first().name

    def get_collect_nums(self):
        '''获取收藏者数量'''
        return self.usercollectarticle_set.count()

    # def get_comment_nums(self):
    #     '''获取回帖评论数量'''
    #     return self.comment.count()


def get_sentinel_article():
    return Article.objects.get_or_create(title='deleted article')[0]


# 2019年12月16日23:29:09 多级评论尝试
class Comment(MPTTModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comment'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )

    # mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    body = RichTextField('评论内容')
    created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def get_follow_nums(self):
        '''获取回答点赞数'''
        return self.userfollowcomment_set.count()

    def __str__(self):
        return self.body[:20]


class UserCollectArticle(models.Model):
    '''用户收藏帖子模型'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name='帖子')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)


class UserFollowComment(models.Model):
    '''用户点赞回帖模型'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                verbose_name='回答')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

