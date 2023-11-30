from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_home, name='account'),
    path('basket', views.basket, name='basket'),
    path('register', views.register, name='register'),
    path('login', views.login_acc, name='login'),
    path('logout', views.logout_acc, name='logout'),
]
