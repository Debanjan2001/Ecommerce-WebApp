from django.contrib.auth import login
from shop.forms import ProductForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView
from . models import Product
import re
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator
# Create your views here.

def home_page(request):
    products = Product.objects.all().order_by('name')
    paginator = Paginator(products,10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
    }

    return render(request, 'shop/homepage.html', context)
    
def product_detailpage(request,pk):
    context = {}
    product = get_object_or_404(Product,pk = pk)
    context['product'] = product
    context['contains'] = False
  
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile,user = request.user)
        context['profile'] = profile
        if profile.products.filter(pk = product.pk) is not None:
            context['contains'] = True     
            # print( Count( profile.products.filter(pk = product.pk)) )
        
        # print(profile.products.all())  
    
    return render(request,'shop/product_detail.html',context)

class create_product(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = 'is_superuser'
    model = Product
    form_class = ProductForm
    template_name = 'shop/create_product.html'
    success_url = reverse_lazy('shop:homepage')


# Class Based Delete Operation ... CRU[D]

# class delete_product(DeleteView):
#     model = Product
#     success_url = reverse_lazy('shop:homepage')

# Function Based Delete Operation ... CRU[D]

class delete_product(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = 'is_superuser'
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse_lazy('shop:homepage')

class update_product(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = 'is_superuser'   
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('shop:homepage')
    template_name = 'shop/product_update.html'


def search_product(request):

    context = {}
    if request.method == 'POST':
        text = request.POST.get("search_text")
        result =[]
    
        for product in Product.objects.all():
            if re.search(text,product.name,re.IGNORECASE):
                result.append(product) 
        
        context['result'] = result

    return render(request,'shop/custom_search.html',context=context)

@login_required
def cart(request):
    context = {}
    profile = Profile.objects.get( user = request.user )
    total_cost = 0
    for product in profile.products.all():
        total_cost += product.price
    context = {
        'profile': profile,
        'products' : profile.products.all(),
        'cost': total_cost,
    }
    return render(request, 'shop/cart.html',context)

@login_required
def add_to_cart(request,pk):

    product = get_object_or_404(Product,pk = pk)
    profile = Profile.objects.get( user = request.user )
    profile.products.add(product)
    return redirect('shop:cart')

@login_required
def remove_from_cart(request,pk):

    product = get_object_or_404(Product,pk = pk)
    profile = Profile.objects.get( user = request.user )
    profile.products.remove(product)

    return redirect('shop:cart')
