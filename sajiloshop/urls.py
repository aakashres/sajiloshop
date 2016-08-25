"""sajiloshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from shoppingcart.views import DashboardView, AddProductView, ProductView, AddCategoryView, CategoryView, \
    CartItemDeleteView
from shoppingcart.views import DashboardView, AddProductView, ProductView, CartView, CheckoutView

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^register/customer/$', "shoppingcart.views.customer_register"),
    url(r'^register/vendor/$', "shoppingcart.views.vendor_register"),
    url(r'^logout/$', "shoppingcart.views.user_logout"),
    url(r'^$', "shoppingcart.views.index"),
    url(r'^login/$', "shoppingcart.views.user_login"),
    url(r'^update/(?P<pk>[\d]+)$', "shoppingcart.views.update"),
    url(r'^dashboard/$',DashboardView.as_view()),
    url(r'^newproduct/$',AddProductView.as_view()),
    url(r'^product/(?P<pk>[\d]+)$',ProductView.as_view()),
    url(r'^newcategory/$',AddCategoryView.as_view()),
    url(r'^category/(?P<pk>[\d]+)$',CategoryView.as_view()),
    url(r'^product/delete/(?P<pk>[\d]+)$',"shoppingcart.views.productdelete"),
    url(r'^cart/$',CartView.as_view() ,name='cart'),
    url(r'^checkout/$',CheckoutView.as_view()),
    url(r'^deleteitem/(?P<pk>[\d]+)$',CartItemDeleteView.as_view()),
]
