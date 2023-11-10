from django.shortcuts import render
from .models import CartItem, Order, OrderItem, Products,Cart,Collection
from core.models import Comment,CommentedItem
from django.contrib.contenttypes.models import ContentType
from core.forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def MainStoreView(request):
    collection_qs = Collection.objects.all()
    products_qs = Products.objects.all()
    return render(request=request,template_name="index2.html",context={'collections':collection_qs,
                                                                      'products':products_qs})

def ProductListView(request):
    qs = Products.objects.all()
    return render(request, "shop-grid-3-columns-sidebar.html",
                  context={'products':qs})
def productDetailView(request,id):
    product_qs = Products.objects.get(id = id)
    contenttype_obj = ContentType.objects.get_for_model(Products)
    comment_qs = CommentedItem.objects.filter(content_type = contenttype_obj,object_id = id) 
    cart = Cart.objects.get(customer = request.user)
    if request.method == 'POST':
        data = request.POST
        action = data.get("button")
        if action == 'cart':
            print("fffffffffffff\nffffffffffffff")
            try:
                cartitem = CartItem.objects.get(product_id = id,cart_id = cart.id)
                cartitem.quantity += 2
                cartitem.save()
            except:
                cartitem = CartItem.objects.create(product_id = id,cart_id = cart.id,quantity = 2)
        elif action == 'comment':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.create(name = form.cleaned_data['name'] ,email= form.cleaned_data['email'],content = form.cleaned_data['content'])
                comment_item = CommentedItem.objects.create(comment = comment,content_type = contenttype_obj,object_id = id)
                messages.success(request, 'Your comment is submited successfully.')
        messages.error(request, "Unsuccessful submition.")
    form = CommentForm()
    return render(request = request, template_name="product-full.html",context={'product':product_qs,
                                                                                'items':comment_qs,
                                                                                'form':form})
def CartView(request):
    cart,created = Cart.objects.get_or_create(customer = request.user)
    cartItems = CartItem.objects.filter(cart = cart)
    finall_price = sum([ item.product.unit_price*item.quantity for item in cart.items.all()])
    if request.method == 'POST':
        order = Order.objects.create(customer = request.user,delivery_id = 1,finall_price = finall_price)
        orderItems = [OrderItem(
                        product = item.product,
                        quantity = item.quantity,
                        unit_price = item.product.unit_price,
                        order = order
                        )for item in cartItems]
        OrderItem.objects.bulk_create(orderItems)
        Cart.objects.filter(id = cart.id).delete()
    return render(request = request,template_name = "cart.html",context={'cartItems':cartItems,'finallPrice':finall_price})

def CollectionListView(request):
    collection_qs = Collection.objects.all()
    return render(request=request,template_name='category-3-columns-sidebar.html',context={'collections':collection_qs})

def ProductFilteringView(request):
    if request.GET.get('collection_id') is not None:
        product_qs = Products.objects.filter(collection_id = request.GET.get('collection_id'))
    elif request.GET.get('q') is not None:
        product_qs = Products.objects.filter(title__icontains = str(request.GET.get('q')))
    return render(request=request,template_name='shop-grid-3-columns-sidebar.html',context={'products':product_qs})