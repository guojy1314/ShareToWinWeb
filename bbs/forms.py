from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import ArticleTopic


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
    content = forms.CharField(label='帖子内容', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3'}), required=False)
    anonymous = forms.BooleanField(label='匿名提问', required=False)


class CommentForm(forms.Form):
    '''回帖表单'''
    content = forms.CharField(label='回帖', widget=CKEditorUploadingWidget(),
                              required=True)
    anonymous = forms.BooleanField(label='匿名回帖', required=False)