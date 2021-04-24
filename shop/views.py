from django.http import request
from shop.forms import ProductForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView,DeleteView
from . models import Product
import re
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator
# Create your views here.


# Email sending
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

def home_page(request):
    products = Product.objects.all().order_by('name')
    paginator = Paginator(products,9)

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

@login_required
@permission_required('is_superuser')
def create_product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            print(product)
            image = form.cleaned_data['image']
            # product = Product.objects.get(pk = product.pk)
            product.image = image
            product.save()

            return redirect('shop:homepage')

        else:
            return render(request,'shop/create_product.html',{ 'form':ProductForm() })


    form = ProductForm()
    return render(request,'shop/create_product.html',{'form':form})



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


#  CBV does not work here with static media files and ignores the request of FILES
#  
@login_required
@permission_required('is_superuser')
def update_product(request,pk):

    product = get_object_or_404(Product,pk = pk)

    form = ProductForm(request.POST or None,request.FILES or None,instance = product)
    if form.is_valid():
        product = form.save(commit=False)
        image = form.cleaned_data['image']
        print(image)
        if Product.objects.filter(image = image) is not None:
            product.image = image
            product.save()
            
        return redirect('shop:homepage')

    return render(request,'shop/product_update.html',{ 'form':form })





def search_product(request):

    context = {}
    if request.method == 'POST':
        text = request.POST.get("search_text")
        result =[]
    
        for product in Product.objects.all():
            if re.search(text,product.name,re.IGNORECASE):
                result.append(product) 
        
        paginator = Paginator(result,9)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
        'page_obj':page_obj,
        'search_text':text,
        'result' : result,
    }

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

@login_required
def checkout(request):

    user = request.user 
    profile = get_object_or_404(Profile,user = user)
    products = profile.products.all()

    cost = 0.0
    for product in products:
        cost += product.price

    print(len(products))
    if len(products) == 0:
        return render(request,'shop/cart.html',context = {'message':'Cart is empty' } )


    mail_subject='Order Successful from Debanjans Ecommerce'
    message = render_to_string('shop/checkout.html',{
        'user' : user,
        'products': products,
        'cost': cost,
            })
    send_mail = user.email
    email = EmailMessage(mail_subject,message,to = [send_mail])
    email.send()

#   Clean up
    profile.products.clear()
    return render(request,'shop/cart.html',context = {'message':'Successfully checked out.Check your email for more details.' } )

   