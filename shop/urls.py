from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.home_page,name = 'homepage'),
    path('product/<int:pk>/',views.product_detailpage,name = 'detailpage'),
    path('product/create/',views.create_product.as_view(),name="create"),
    path('product/delete/<int:pk>/',views.delete_product.as_view(),name='delete'),
    path('product/update/<int:pk>/',views.update_product.as_view(),name='update'),
    path('product/search/',views.search_product,name="search_product"),
    path('cart/',views.cart,name="cart"),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>',views.remove_from_cart,name='remove_from_cart'),

]