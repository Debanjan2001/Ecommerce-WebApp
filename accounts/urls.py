from django.urls import path
from django.contrib.auth import views as auth
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.user_login,name="user_login"),
    path('logout/',views.user_logout,name="user_logout"),
    path('signup/',views.user_signup,name="user_signup"),
    path('profile/',views.profilepage,name="profile"),
    path('success/',views.signup_success,name="signup_success"),
    
]




