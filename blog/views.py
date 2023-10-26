from django.shortcuts import render,redirect
from .forms import PostCreateForm,CommentForm
from django.contrib import messages
from .models import Post
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
    if request.method == 'POST':
        form = CommentForm(data = request.POST,post_id = id)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment is submited successfully.')
        messages.error(request, "Unsuccessful submition.")
    form = CommentForm()
    return render(request=request,template_name='post-full-width.html',context={'post':post_qs,'form':form})