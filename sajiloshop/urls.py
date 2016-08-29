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
from shoppingcart.views import DashboardView, AddProductView, ProductView, CartView, CheckoutView,\
    UpdateView,LogoutView,AddCategoryView, CategoryView,CartItemDeleteView,IndexView,LoginView,CustomerRegisterView,VendorRegisterView

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^register/customer/$',CustomerRegisterView.as_view()),
    url(r'^register/vendor/$', VendorRegisterView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^$', IndexView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^update/(?P<pk>[\d]+)$',UpdateView.as_view()),
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
