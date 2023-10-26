from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.MainStoreView),
    path('products/',views.ProductListView),
    path('products/<int:id>',views.productDetailView),
    path('carts/',views.CartView),
    path('collections/',views.CollectionListView),
    path('products',views.ProductFilteringView)
]