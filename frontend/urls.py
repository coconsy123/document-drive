from django.contrib.auth.views import LogoutView
from django.urls import path
from frontend.views import *

urlpatterns = [
    path('login/', login_page, name='frontend-login'),
    path('register/', register_page, name='frontend-register'),
    path('logout/', logout_page, name='frontend-logout')
]

