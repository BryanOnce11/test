"""
URL configuration for electric_bill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from electric_bill_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='root'),
    path('index/', views.index, name='index'),
    path('process/', views.process, name='process'),
    path('register/', views.register, name='register'),
    path('register_process/', views.register_process, name='register_process'),
    path('logout/', views.logout, name= 'logout'),
    path('home/', views.home, name='home'),
    path('clients/', views.clients, name='clients'),
    path('edit-owner/', views.edit_owner, name='edit_owner'),
    path('delete_owner/<int:owner_id>/', views.delete_client, name='delete_owner'),
    path('users/', views.users, name='users'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('billing/', views.billing, name='billing'),
    path('paybill/<int:owner_id>/', views.paybill, name='paybill'),
    path('addbill/<int:owner_id>/', views.addbill, name='addbill'),
    path('viewbill/<int:owner_id>/', views.view_bill, name='viewbill'),
    path('viewpayment/<int:bill_id>/', views.view_payment, name='view_payment'),
    path('delbill/<int:bill_id>/', views.del_bill, name='delbill'),
]
