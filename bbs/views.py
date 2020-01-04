from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# cache
from django.views.decorators.cache import cache_page

from helper.paginator_helper import paginator_helper
from user.models import User
from .forms import PubArticleForm, ArticleCommentForm
from .models import Article, Comment, ArticleTopic,  \
    UserCollectArticle, UserFollowComment


@cache_page(5 * 60, key_prefix='article_list')
def article_list(request):
    '''帖子列表'''
    articles = Article.objects.all().order_by('-pub_time').annotate(
        comment_nums=Count('comment', distinct=True),
        collect_nums=Count('usercollectarticle', distinct=True))
    hot_articles = Article.objects.all().annotate(
        comment_nums=Count('comment', distinct=True),
        collect_nums=Count('usercollectarticle', distinct=True)).order_by(
        '-comment_nums')

    # 分页
    articles_page = paginator_helper(request, articles,
                                      per_page=settings.QUESTION_PER_PAGE)
    hot_articles_page = paginator_helper(request, hot_articles,
                                          per_page=settings.QUESTION_PER_PAGE)

    context = {}
    context['articles_page'] = articles_page
    context['hot_articles_page'] = hot_articles_page
    return render(request, 'bbs/article_list.html', context)


def article_detail(request, article_id):
    '''帖子详情'''
    article = get_object_or_404(Article, pk=article_id)
    # get请求一次, 浏览量+1
    article.read_nums += 1
    article.save()

    # 判断用户是否收藏了帖子
    has_collect_article = False
    if request.user.is_authenticated:
        if UserCollectArticle.objects.filter(user=request.user,
                                             article=article):
            has_collect_article = True

    # 帖子的回复
    article_comments = Comment.objects.filter(article=article)
    # article_comments = cache.get('article_comment' + str(article_id))
    # if not article_comments:
    #     article_comments = Comment.objects.filter(article=article).annotate(
    #         follow_nums=Count('userfollowcomment', distinct=True))\
    #         # .annotate( \
    #         # comment_nums=Count('commentcomment', distinct=True))
    #     cache.set('article_comments' + str(article_id), article_comments,
    #               5 * 60)

    # # 问题下回答排序
    # sort_type = request.GET.get('sort_type', '')
    # # 如果按点赞数数排序
    # if sort_type == 'follows':
    #     article_comments = article_comments.order_by('-follow_nums')
    #
    # # 默认排序, 按时间排序
    # else:
    #     article_comments = article_comments.order_by('-created')

    # 分页
    page = paginator_helper(request, article_comments,
                            per_page=settings.ANSWER_PER_PAGE)
    comment_form = ArticleCommentForm()

    context = {}
    context['article'] = article
    context['has_collect_article'] = has_collect_article
    # context['sort_type'] = sort_type
    context['page'] = page
    context['comment_form'] = comment_form
    # context['relate_questions'] = relate_questions
    # return render(request, 'bbs/article_detail.html', context)
    return render(request, 'bbs/detail.html', context)


# def comment_detail(request, comment_id):
#     '''回答详情'''
#     comment = get_object_or_404(Comment, pk=comment_id)
#     article = comment.article
#
#     has_collect_article = False
#     has_follow_comment = False
#     if request.user.is_authenticated:
#         if UserCollectArticle.objects.filter(user=request.user,
#                                              article=article):
#             has_collect_article = True
#         if UserFollowComment.objects.filter(user=request.user, comment=comment):
#             has_follow_comment = True

    # # 归属问题话题的相关问题, 按阅读量排序
    # # 回答归属question归属话题, 取第一个话题
    # question_topic = question.topics.all().first()
    # # 话题相关question, 取前5个, 并排除自身
    # relate_questions = cache.get('relate_questions' + str(answer_id))
    # if not relate_questions:
    #     relate_questions = question_topic.question_set.exclude(
    #         id=answer.question_id).order_by('-read_nums')[:5]
    #     cache.set('relate_questions' + str(answer_id), relate_questions, 5 * 60)
    # 评论表单
    # comment_form = CommentForm()
    # # 评论分页
    # answer_comments = comment.answercomment_set.all().order_by('-add_time')
    # page = paginator_helper(request, answer_comments,
    #                         per_page=settings.COMMENT_PER_PAGE)
    #
    # context = {}
    # context['comment'] = comment
    # context['has_collect_article'] = has_collect_article
    # context['has_follow_comment'] = has_follow_comment
    # context['relate_questions'] = relate_questions
    # context['comment_form'] = comment_form
    # context['page'] = page
    # return render(request, 'bbs/comment_detail.html', context)


@login_required
def add_follow_artcomment(request):
    '''赞同回答'''
    comment_id = int(request.GET.get('comment_id', ''))
    comment = get_object_or_404(Comment, id=comment_id)
    comment_follow_existed = UserFollowComment.objects.filter(user=request.user,
                                                            comment=comment)
    print(comment_follow_existed.count())
    if comment_follow_existed:
        comment_follow_existed.delete()
        return JsonResponse({'status': 'success', 'reason': 'cancel'})
    else:
        comment_follow = UserFollowComment(user=request.user, comment=comment)
        comment_follow.save()
        return JsonResponse({'status': 'success', 'reason': 'add'})


@login_required
def cancel_follow_answer(request):
    '''取消赞同'''
    comment_id = int(request.GET.get('comment_id', ''))
    comment = get_object_or_404(Comment, id=comment_id)
    comment_follow_existed = UserFollowComment.objects.filter(user=request.user,
                                                            comment=comment)
    if comment_follow_existed:
        comment_follow_existed.delete()
        return JsonResponse({'status': 'success', 'reason': 'cancel'})
    else:
        return JsonResponse({'status': 'success', 'reason': 'nothing'})


# @login_required
# def comment_answer(request, answer_id):
#     '''评论回答'''
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.cleaned_data.get('comment')
#             answer = get_object_or_404(Answer, id=answer_id)
#             answer_comment = AnswerComment(user=request.user, answer=answer,
#                                            comment=comment)
#             answer_comment.save()
#             return JsonResponse({'status': 'success', 'message': '你的评论已提交'})
#         else:
#             return JsonResponse({'status': 'fail', 'message': '评论不能为空'})


@login_required
def collect_article(request):
    '''收藏帖子'''
    article_id = int(request.GET.get('article_id', ''))
    article = get_object_or_404(Article, id=article_id)
    collect_article_existed = UserCollectArticle.objects.filter(user=request.user,
                                                                article=article)
    if collect_article_existed:
        collect_article_existed.delete()
        return JsonResponse({'status': 'success', 'message': '收藏'})
    else:
        collect_article = UserCollectArticle(user=request.user, article=article)
        collect_article.save()
        return JsonResponse({'status': 'success', 'message': '已收藏'})


@login_required
def pub_article(request):
    '''发布帖子'''
    pub_article_form = PubArticleForm()

    if request.method == 'POST':
        pub_article_form = PubArticleForm(request.POST)
        if pub_article_form.is_valid():
            article = Article()
            article.author = request.user
            article.title = pub_article_form.cleaned_data.get('title')
            article.content = pub_article_form.cleaned_data.get('content')
            article.is_anonymous = pub_article_form.cleaned_data.get(
                'anonymous')
            article.save()
            # 保存多对多关系前保存article对象
            article.topics.set(pub_article_form.cleaned_data.get('topics'))
            messages.info(request, '你的帖子已发布')
            return redirect(reverse('article_detail', args=(article.id,)))
        messages.info(request, '你的输入有误')

    context = {}
    context['pub_article_form'] = pub_article_form
    return render(request, 'bbs/pub_article.html', context)
#
#
# @login_required
# def comment_article(request, article_id):
#     '''回复帖子'''
#     comment_form = CommentForm()
#     # article = get_object_or_404(Article, id=article_id)
#     article = article_id
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = Comment()
#             comment.article = article
#             comment.author = request.user
#             comment.content = comment_form.cleaned_data.get('content')
#             comment.is_anonymous = comment_form.cleaned_data.get('anonymous')
#             comment.save()
#             messages.info(request, '你的回帖已提交')
#             return redirect(reverse('article_detail', args=(article.id,)))
#
#     context = {}
#     context['article'] = article
#     context['comment_form'] = comment_form
#     return redirect(reverse('article_detail', args=(article.id,)))


@login_required
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(Article, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = ArticleCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = Comment()
            # new_comment = comment_form.save(commit=False)
            new_comment.body = comment_form.cleaned_data.get('body')
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect(reverse('article_detail', args=(article_id,)))
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = ArticleCommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'bbs/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")
