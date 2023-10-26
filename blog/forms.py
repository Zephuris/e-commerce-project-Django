from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Post,Comment
from django.contrib.auth.models import User

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    content = forms.CharField(required=True, widget=forms.Textarea(
                                attrs={"id":"blog-content",
                                       "class":"form-control form-control-lg"}))
    author_id = forms.IntegerField(required=True)

    class Meta:
        model = Post
        fields = ('title','content','author_id')
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PostCreateForm, self).__init__(*args,**kwargs)
        self.fields['author_id'].initial = self.request.user.id
   
    def save(self, commit: bool = ...) -> Any:
        post = super(PostCreateForm,self).save(commit=False)
        post.title = self.cleaned_data['title']
        post.content = self.cleaned_data['content']
        post.author_id = self.cleaned_data['author_id']
        if commit:
            post.save()
        return post
class CommentForm(forms.ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    body = forms.CharField(widget=forms.Textarea)
    post_id = forms.IntegerField(required=True)
    class Meta:
        model = Comment
        fields = ['name','email','body','post_id']

    def __init__(self, *args, **kwargs):
        self.post_id = kwargs.pop("post_id")
        super(PostCreateForm, self).__init__(*args,**kwargs)
        self.fields['post_id'].initial = self.post_id
        
    def save(self, commit: bool = ...) -> Any:
        comment = super(CommentForm,self).save(commit=False)
        comment.title = self.cleaned_data['body']
        comment.content = self.cleaned_data['content']
        comment.author_id = self.cleaned_data['author_id']
        if commit:
            comment.save()
        return comment