from django.http import request
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from . models import Product
import re
# Create your views here.

class Homepage(ListView):
    model = Product
    template_name = 'shop/homepage.html'

class detailpage(DetailView):
    model = Product

class createproduct(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('shop:homepage')

class deleteproduct(DeleteView):
    model = Product
    success_url = reverse_lazy('shop:homepage')

class updateproduct(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('shop:homepage')
    template_name = 'shop/product_update.html'


def search_text(request):
    if request.method == 'POST':
        text = request.POST.get("search_text")
        result =[]
    
        for product in Product.objects.all():
            if re.search(text,product.name,re.IGNORECASE):
                result.append(product) 
                
        return render(request,'shop/custom_search.html',{'search_text':text,'result':result})
    else:
        return render(request,'shop/custom_search.html')

def cart(request):
    return render(request, 'shop/cart.html')