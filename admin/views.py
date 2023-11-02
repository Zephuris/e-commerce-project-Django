from django.shortcuts import render,get_object_or_404
from .forms import ProductForm
from store.models import Products
# Create your views here.
def ProductCreateView(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
        form = ProductForm()
        return render(request=request,template_name="product-creating.html",context={'form':form})
    return render(request,'403.html')

def ProductEditView(request,id):
    if request.user.is_superuser:
        product = get_object_or_404(Products,id = id)
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES,instance = product)
            if form.is_valid():
                form.save()
        form = ProductForm(instance=product)
        return render(request=request,template_name="product-creating.html",context={'form':form})

    return render(request,'403.html')
