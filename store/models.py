from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from uuid import uuid4

class Collection (models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Products', on_delete=models.SET_NULL, null=True, related_name='ProductItems', blank=True)
    def __str__(self) -> str:
        return self.title
    
class Products (models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return self.title
# class Customer (models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,unique=True)
#     phoneNumber = models.PositiveBigIntegerField()

class Delivery(models.Model):
    address = models.CharField(max_length=255)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT , related_name='delivery' )
    
class Order (models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add = True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT , related_name='orders')
    delivery = models.ForeignKey(Delivery,on_delete=models.PROTECT,related_name='order')
    finall_price = models.DecimalField(max_digits=9, decimal_places=2)
class OrderItem (models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT , related_name='items')
    product = models.ForeignKey(Products, on_delete =models.PROTECT , related_name='orderitem')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)

class Cart (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4 )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT , related_name='cart' )
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , related_name= 'items')
    product = models.ForeignKey(Products, on_delete =models.PROTECT )
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])




