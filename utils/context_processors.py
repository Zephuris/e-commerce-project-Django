from django.contrib.auth.models import User,AnonymousUser
from store.models import Cart
def user_context(request):
    print(request.user)
    return {'user_context':request.user}

def cart_context(request):
    if request.user.is_active:
        cart,created = Cart.objects.get_or_create(customer = request.user)
        finall_price = sum([ item.product.unit_price*item.quantity for item in cart.items.all()])
        return {'cart_items_context':cart.items.all(),'price_context':finall_price}
    else:
        return{'cart_items_context':0,'price_context':0}
