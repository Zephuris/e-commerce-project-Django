from django.urls import path
from . import views
urlpatterns= [
    path('',views.MainAdminView),
    path('product/',views.ProductCreateView),
    path('product/<int:id>',views.ProductEditView),
    path('collection/',views.CollectionCreateView),
    path('collection/<int:id>',views.CollectionEditView),
]