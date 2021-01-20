from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.Homepage.as_view(),name = 'homepage'),
    path('product/<int:pk>/',views.detailpage.as_view(),name = 'detailpage'),
    path('create/',views.createproduct.as_view(),name="create"),
    path('delete/<int:pk>/',views.deleteproduct.as_view(),name='delete'),
    path('update/<int:pk>/',views.updateproduct.as_view(),name='update'),
    path('search/',views.search_text,name="searching"),
    path('cart/',views.cart,name="cart"),
]