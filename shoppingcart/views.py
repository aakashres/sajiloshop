from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
# Create your views here.
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from shoppingcart.forms import UserForm, CustomerForm, VendorForm
from django.contrib.auth.decorators import login_required
import json
from shoppingcart.models import Product, Customer, Vendor, PersonalInfo, Order, OrderItem, Category
from django.core import serializers
from django.db.utils import IntegrityError

class CustomerRegisterView(TemplateView):
    template_name = "register.html"

    def get(self,request):
        user_form = UserForm()
        profile_form = CustomerForm()
        return render(request,'register.html',{'user_form': user_form, 'profile_form': profile_form})

    def post(self,request):
        context = RequestContext(request)
        registered = False

        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            profile_form = CustomerForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = CustomerForm()
        return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

class VendorRegisterView(TemplateView):
    template_name = "register.html"

    def get(self,request):
        user_form = UserForm()
        profile_form = VendorForm()
        return render(request,'register.html',{'user_form': user_form, 'profile_form': profile_form})

    def post(self,request):

        context = RequestContext(request)
        registered = False

        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            profile_form = VendorForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = UserForm()
            profile_form = VendorForm()
        return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

class LoginView(TemplateView):
    template_name = "login.html"

    def post(self,request):
        context = RequestContext(request)

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    customer = Customer.objects.filter(user = user)
                    if customer:
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect('/dashboard')
                else:
                    return HttpResponse("Login Again")
            else:
                print("Invalid login details: {0}, {1}".format(username, password))
                return HttpResponse("Invalid login details supplied.")

        else:
            return render_to_response('login.html', {}, context)

class IndexView(TemplateView):
    def get(self, request):
        product = Product.objects.all().order_by('-created')
        category = Category.objects.all().order_by('-created')
        context1 =[]

        for new in category:
            productlist = Product.objects.filter(category=new)
            if productlist:
                list1 = list(productlist)
                context1.append(list1)
            else:
                context1 = []

        context = {'product': product, 'category':category,'productlist':context1}
        return render(request,'index.html', context)

class LogoutView(LoginRequiredMixin,TemplateView):
    login_url = '/login/'

    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')

class UpdateView(LoginRequiredMixin,TemplateView):
    template_name = "update.html"
    login_url = '/login/'

    def get(self, request,pk):
        user = request.user
        user_form = UserForm(instance=user)
        try:
            customer = Customer.objects.filter(user = user)
            profile_form = CustomerForm(instance=user.customer)
        except:
            customer = Vendor.objects.filter(user = user)
            profile_form = VendorForm(instance=user.vendor)
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'update.html', context)

    def post(self,request,pk):
        user = request.user

        user_form = UserForm(instance=user)
        customer = Customer.objects.filter(user = user)
        vendor = Vendor.objects.filter(user = user)
        updated = False

        if customer:
            profile_form = CustomerForm(instance=user.customer)

            if request.method == 'POST':
                user_form = UserForm(data=request.POST, instance=user)
                profile_form = CustomerForm(data=request.POST, instance=user.customer)

                if user_form.is_valid() and profile_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    updated = True

        else:
            profile_form = VendorForm(instance=user.vendor)

            if request.method == 'POST':
                user_form = UserForm(data=request.POST, instance=user)
                profile_form = VendorForm(data=request.POST, instance=user.vendor)

                if user_form.is_valid() and profile_form.is_valid():
                    user = user_form.save()
                    user.set_password(user.password)
                    user.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    updated = True

        context = {'user_form': user_form, 'profile_form': profile_form,'updated':updated}
        return render(request, 'update.html', context)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = '/login/'
    def get(self, request):
        user = self.request.user
        try:
            CheckCustomer = True
            customer1 = Customer.objects.get(user = user)
            order = OrderItem.objects.filter(order__customer=customer1).order_by('-created')
            context = {'data': customer1 ,'order':order, 'customer':CheckCustomer}
            return render(request,'dashboard.html',context)

        except ObjectDoesNotExist:
            CheckCustomer = False
            vendor = Vendor.objects.get(user = user)
            products = Product.objects.filter(vendor=vendor).order_by('-created')
            order = OrderItem.objects.filter(product__vendor=vendor).order_by('-created')
            context = {'data':vendor,'customer':CheckCustomer , 'products':products,'order':order}
            return render(request,'dashboard.html',context)

class AddCategoryView(LoginRequiredMixin,TemplateView):
    template_name = 'addcategory.html'
    model = Category
    added = False

    def get(self, request):
        category = Category.objects.all()
        return render(request,'addcategory.html',{'category':category})

    def post(self, request):
        category_name = request.POST.get('category_name', None)
        category = Category(category_name= category_name)
        category.description = request.POST['description']
        subparent = request.POST.get('self',None)

        try:
            checkCategory = Category.objects.get(category_name = subparent)
            if checkCategory:
                category.parent = checkCategory
        except Category.DoesNotExist:
            category.parent = None

        category.save()
        added = True
        return render(request,'addcategory.html', {'added':added})

class CategoryView(TemplateView):
    template_name = "category.html"

    def get(self, request,pk):
        category = Category.objects.get(pk = pk)
        product = Product.objects.filter(category = category)

        categories = Category.objects.all()
        context ={'category':category, 'product':product,'categories':categories}
        return render(request,'category.html',context)



class AddProductView(LoginRequiredMixin,TemplateView):
    template_name = "addproduct.html"
    model = Product
    added = False
    login_url = '/login/'

    def get(self, request):
        category = Category.objects.all()
        return render(request,'addproduct.html',{'category':category})

    def post(self,request):
        product_name = request.POST['product_name']
        product = Product(product_name= product_name)
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.discount = request.POST['discount']
        product.stock = request.POST['stock']
        product.feature = request.POST['feature']
        product.tags = request.POST['tags']

        category= request.POST['category']
        checkCategory = Category.objects.get(category_name = category)
        if checkCategory:
            product.category = checkCategory

        vendor = Vendor.objects.get(user = request.user)
        if vendor:
            product.vendor = vendor

        product.save()
        added = True
        return render(request,'addproduct.html',{'added':added})

class ProductView(TemplateView):
    template_name = 'product.html'

    def get(self, request,pk):
        product = Product.objects.get(pk =pk)
        context ={'product':product}
        return render(request,'product.html',context)

    def post(self,request,pk):
        product = Product.objects.get(pk = pk)
        quantity = request.POST['quantity']
        cart_data = [{'product':product.id,'quantity':quantity,'price':int(quantity)*int(product.price),'product_name':product.product_name}]

        try:
            customer = Customer.objects.get(user=request.user)

            prev_cart = customer.cart

            if prev_cart:
                for i, item in enumerate(prev_cart):
                    if prev_cart[i]['product']== product.id :
                        change_quantity= int(quantity) + int(prev_cart[i]['quantity'])
                        prev_cart[i]['quantity']= change_quantity
                        change_price= int(quantity)*int(product.price) + int(prev_cart[i]['price'])
                        prev_cart[i]['price']= change_price
                        cart_data = []

                customer.cart = cart_data.extend(prev_cart)

            customer.cart = cart_data
            customer.save()
            return HttpResponseRedirect('/cart/')

        except:
            vendor = True
            return render(request,'product.html',{'vendor':vendor,'product':product})

def productdelete(request, pk=None):
    product = Product.objects.get(pk=pk)
    if product.vendor == request.user.vendor:
        product.delete()
    return HttpResponseRedirect('/dashboard/')

class CartView(LoginRequiredMixin,TemplateView):
    template_name = 'cart.html'
    login_url = '/login/'

    def get(self, request):
        try:
            customer = request.user.customer
            cart_data=customer.cart
            total = 0
            count=0
            noitem = True
            if cart_data:
                noitem = False
                for i, item in enumerate(cart_data):
                    total = cart_data[i]['price']+total
                    count = count + 1
            request.session['cartcount']= count
            return render(request,'cart.html', {'cart_data':cart_data,'total':total,'noitem':noitem})
        except:
            vendor = True
            return render(request,'cart.html',{'vendor':vendor})

    def post(self,request):
            return HttpResponseRedirect('/checkout/')

class CartItemDeleteView(TemplateView,LoginRequiredMixin):
    template_name = 'cart.html'
    login_url = '/login/'

    def get(self, request,pk):
        customer = Customer.objects.get(user=request.user)
        prev_cart = customer.cart
        product = Product.objects.get(id=pk)
        if prev_cart:
            for i, item in enumerate(prev_cart):
                if prev_cart[i]['product']== product.id :
                    del prev_cart[i]

        customer.cart = prev_cart
        customer.save()
        return HttpResponseRedirect('/cart/')


class CheckoutView(LoginRequiredMixin,TemplateView):
    template_name = 'checkout.html'
    login_url = '/login/'

    def get(self, request):
        try:
            customer = Customer.objects.get(user = request.user)
            context = {'customer':customer}
            return render(request,'checkout.html',context)
        except:
            vendor = True
            return render(request,'checkout.html',{'vendor':vendor})

    def post(self,request):
        order = Order(customer=request.user.customer)
        customer = Customer.objects.get(user = request.user)
        cart_data = customer.cart
        total = 0
        for i, item in enumerate(cart_data):
            total = cart_data[i]['price']+total

        order.total_price = total
        order.save()

        for i, item in enumerate(cart_data):
            orderitem = OrderItem(order = order)
            product = Product.objects.get(id=cart_data[i]['product'])
            orderitem.product = product
            orderitem.quantity= cart_data[i]['quantity']
            orderitem.price = cart_data[i]['price']
            orderitem.save()

        del request.session['cartcount']
        customer.cart =[]
        customer.save()

        added = True
        return render(request,'checkout.html',{'added':added})
