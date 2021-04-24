from accounts.models import Profile
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . forms import  ActivationForm, SignUpForm, UserLoginForm
from . models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

#Email imports
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

# Create your views here.

def user_login(request):

    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST' :
        
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
            
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('shop:homepage')

        else:            
            return render(request,'accounts/login.html',{'form':form,'error':True})

    else:
        form = UserLoginForm()
        return render(request,'accounts/login.html',{'form':form})


@login_required
def user_logout(request):

    logout(request)
    return redirect('shop:homepage')

def user_signup(request):

    form = None

    if request.method == 'POST':

        form = SignUpForm(request.POST)
          
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            queryname = User.objects.filter(username=username )
            querymail = User.objects.filter(email=email)

            if queryname or querymail:
                form = SignUpForm()
                username_exists = False
                email_exists = False
                if querymail:
                    email_exists = True
                if queryname:
                    username_exists = True
                context_dict={'username_exists':username_exists,'email_exists':email_exists,'form':form}
                return render(request,'accounts/signup.html',context = context_dict)

            user = User.objects.create(username = username,email = email)
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active=False
            user.save()

            current_site = get_current_site(request)
            mail_subject='Activate Your Account at Debanjan:Ecommerce-WebApp'
            message = render_to_string('registration/activate_account.html',{
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'request':request,
            })

            send_mail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject,message,to = [send_mail])
            email.send()
            
            return render(request,'accounts/confirm_account_message.html',context={})
            
    else:
        form = SignUpForm()
    
    context = {'form':form}
    return render(request,'accounts/signup.html',context)


def signup_success(request):
    return render(request,'accounts/signup_success.html')

def signup_failure(request):
    return render(request,'accounts/signup_failure.html')


def confirm_account_message(request):
    return render(request,'accounts/confirm_account_message.html')

def activate_account(request,uidb64,token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(User,pk = uid)
    if user.is_active == False and default_token_generator.check_token(user,token):
        user.is_active = True
        profile = Profile.objects.create(user =user)
        profile.set(first_name = user.first_name,last_name = user.last_name)
        profile.save()
        user.save()
        return redirect('accounts:signup_success')
    else:
        return redirect('accounts:signup_failure')


def manual_activation_failure(request):
    return render(request,'accounts/manual_activation_failure.html')

def manually_activate_account(request):

    form = None

    if request.method == 'POST':

        form = ActivationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            user = None
            if len(username)>0:
                try:
                    user = User.objects.get(username = username)
                except ObjectDoesNotExist:
                    return redirect('accounts:manual_activation_failure')

            if len(email)>0 and user is None:
                try:
                    user = User.objects.get(email = email)
                except ObjectDoesNotExist:
                    return redirect('accounts:manual_activation_failure')

            if user is None:
                return redirect('accounts:signup_failure')

            if user.is_active == True:
                return redirect('accounts:signup_failure')

            current_site = get_current_site(request)
            mail_subject='Activate Your Account at Debanjan:Ecommerce-WebApp'
            message = render_to_string('registration/activate_account.html',{
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'request':request,
            })

            send_mail = user.email
            email = EmailMessage(mail_subject,message,to = [send_mail])
            email.send()

            return redirect('accounts:confirm_account')

        else:
            form = ActivationForm()

    else:

        form = ActivationForm()

    return render(request,'accounts/manual_activation.html',context = {'form':form})


def profilepage(request):
    profile = get_object_or_404(Profile,user = request.user)
    context = {
        'user' : request.user,
        'profile' : profile,
    }
    return render(request,'accounts/profile.html',context)
