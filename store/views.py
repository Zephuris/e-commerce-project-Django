from django.shortcuts import render
from .models import CartItem, Order, OrderItem, Products,Cart,Collection
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
    cart,created = Cart.objects.get_or_create(customer = request.user)
    if request.method == 'POST':
        try:
            cartitem = CartItem.objects.get(product_id = id,cart_id = cart.id)
            cartitem.quantity += 2
            cartitem.save()
        except:
            cartitem = CartItem.objects.create(product_id = id,cart_id = cart.id,quantity = 2)

    return render(request = request, template_name="product-full.html",context={'product':product_qs,
                                                                                'user':request.user,
                                                                                'cartItem':cart.items.all()})
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