from django.http import request
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from . models import Product
# Create your views here.

class Homepage(ListView):
    model = Product
    template_name = 'shop/homepage.html'


class detailpage(DetailView):
    model = Product

class createproduct(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('shop:home') 

class deleteproduct(DeleteView):
    model = Product
    success_url = reverse_lazy('shop:home')

class updateproduct(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('shop:home')
    template_name = 'shop/product_update.html'

def search_text(request):
    if request.method == 'POST':
        text = request.POST.get("search_text")
        print(text)
        print("Hel")
        result =[]
        
        for product in Product.objects.all():
            if text == product.name[0]:
                result.append(product) 
        return render(request,'shop/searchpage.html',{'result':result})
    else:
        return render(request,'shop/searchpage.html')

def cart(request):
    return render(request, 'shop/cart.html')