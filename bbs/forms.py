from django import forms
from .models import ArticleTopic
from ckeditor.fields import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Comment


class PubArticleForm(forms.Form):
    '''发帖表单'''
    title = forms.CharField(label='讨论帖标题', widget=forms.TextInput(
        attrs={'class': 'form-control'}), max_length=200, required=True)
    topics = forms.ModelMultipleChoiceField(queryset=ArticleTopic.objects.all(),
                                            to_field_name='name', label='添加分类',
                                            required=True, \
                                            widget=forms.SelectMultiple(attrs={
                                                'class': 'selectpicker form-control',
                                                'data-live-search': 'true',
                                                'title': '请选择分类'}))
    content = forms.CharField(label='帖子内容', widget=CKEditorUploadingWidget(),
                              required=False)
    anonymous = forms.BooleanField(label='匿名提问', required=False)


class ArticleCommentForm(forms.Form):
    '''回帖表单'''
    body = forms.CharField(label='回帖', widget=CKEditorWidget(), required=True)
    # class Meta:
    #     model = Comment
    #     fields = ['body']