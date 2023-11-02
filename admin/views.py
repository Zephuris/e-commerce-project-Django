from django.shortcuts import render,get_object_or_404
from .forms import CollectionForm, ProductForm
from store.models import Products,Collection,Order
# Create your views here.
def MainAdminView(request):
    product = Products.objects.all()
    collection = Collection.objects.all()
    orders = Order.objects.all()
    return render(request,'admin-index.html',context={'products':product,
                                                      'collections':collection,
                                                      'orders':orders})

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

def CollectionCreateView(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    form = CollectionForm()
    return render(request,'collection-creating.html',context={'form':form})

def CollectionEditView(request,id):
    collection = Collection.objects.get(id = id)
    if request.method == 'POST':
        form = CollectionForm(request.POST,request.FILES,instance=collection)
        if form.is_valid():
            form.save()
    form = CollectionForm(instance=collection)
    return render(request,'collection-creating.html',context={'form':form})