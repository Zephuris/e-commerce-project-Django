from django.shortcuts import render,get_object_or_404
from .forms import EditProductForm, ProductCreationForm
from store.models import Products
# Create your views here.
def ProductCreateView(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductCreationForm(request.POST)
            if form.is_valid():
                product = Products.objects.create(title = form.cleaned_data['title'],
                                    description = form.cleaned_data['description'],
                                    unit_price = form.cleaned_data['unit_price'],
                                    slug = form.cleaned_data['slug'],
                                    inventory = form.cleaned_data['inventory'],
                                    collection_id = form.cleaned_data['collection'].values('id'))
        form = ProductCreationForm()
        return render(request=request,template_name="product-creating.html",context={'form':form})
    return render(request,'403.html')
def ProductEditView(request,id):
    if request.user.is_superuser:
        product = get_object_or_404(Products,id = id)
        if request.method == 'POST':
            form = EditProductForm(request.POST,instance = product)
            if form.is_valid():
                form.save()
        form = EditProductForm(instance=product)
        return render(request=request,template_name="product-creating.html",context={'form':form})

    return render(request,'403.html')
