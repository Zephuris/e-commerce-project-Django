from django.shortcuts import render,redirect
from .forms import PostCreateForm
from core.forms import CommentForm
from django.contrib import messages
from .models import Post
from core.models import Comment,CommentedItem
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def PostCreateView(request):
    if request.method == 'POST':
        form = PostCreateForm(data = request.POST,request = request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = PostCreateForm(request = request)
    return render(request=request ,
                   template_name="blog-creating.html",
                   context={"form" : form})

def PostListView(request):
    posts_qs = Post.objects.all()
    return render(request=request,template_name='blog-grid-left-sidebar.html',context={'posts':posts_qs})

def PostDetailView(request,id):
    post_qs = Post.objects.get(id = id)
    contenttype_obj = ContentType.objects.get_for_model(Post)
    comment_qs = CommentedItem.objects.filter(content_type = contenttype_obj,object_id = id)
    print(comment_qs)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(name = form.cleaned_data['name'] ,email= form.cleaned_data['email'],content = form.cleaned_data['content'])
            comment_item = CommentedItem.objects.create(comment = comment,content_type = contenttype_obj,object_id = id)
            messages.success(request, 'Your comment is submited successfully.')
        messages.error(request, "Unsuccessful submition.")
    form = CommentForm()
    return render(request=request,template_name='post-full-width.html',context={'post':post_qs,'form':form,'items':comment_qs})
