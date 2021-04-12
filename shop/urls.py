from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.Homepage.as_view(),name = 'homepage'),
    path('product/<int:pk>/',views.detailpage.as_view(),name = 'detailpage'),
    path('product/create/',views.createproduct.as_view(),name="create"),
    path('product/delete/<int:pk>/',views.delete_product,name='delete'),
    path('product/update/<int:pk>/',views.updateproduct.as_view(),name='update'),
    path('product/search/',views.search_product,name="search_product"),
    path('cart/',views.cart,name="cart"),
]