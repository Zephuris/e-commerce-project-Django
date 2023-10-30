from django.urls import path
from . import views
urlpatterns= [
    path('product/',views.ProductCreateView),
    path('product/<int:id>',views.ProductEditView)
]