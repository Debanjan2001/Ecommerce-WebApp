from django.urls import path
from django.contrib.auth import views as auth
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.user_login,name="user_login"),
    path('logout/',views.user_logout,name="user_logout"),
    path('signup/',views.user_signup,name="user_signup"),
    path('profile/',views.profilepage,name="profile"),
    path('signup/success/',views.signup_success,name="signup_success"),
    path('signup/failure/',views.signup_failure,name="signup_failure"),
    path('change_password/',auth.PasswordResetView.as_view(),name = 'password_change'),
    path('activate/<uidb64>/<token>/',views.activate_account,name = 'activate_account'),
    path('confirm_account_message/',views.confirm_account_message,name = 'confirm_account'),
    path('manual_activation/',views.manually_activate_account,name = 'manual_activation'),
    path('manual_activation_failure/',views.manual_activation_failure,name = 'manual_activation_failure'),


]




