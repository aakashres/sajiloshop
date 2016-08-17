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

from shoppingcart.models import Product, Customer, Vendor, PersonalInfo, Order, OrderItem, Category


def customer_register(request):

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

def vendor_register(request):

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

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                customer = Customer.objects.filter(user = user)
                if customer:
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/dashboard')
            else:

                return HttpResponse("Login Again")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)


def index(request):
    product = Product.objects.all().order_by('-created')
    category = Category.objects.all().order_by('-created')
    context = {'product': product, 'category':category}
    return render(request,'index.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def update(request, pk=None):
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
        if user.customer:
            CheckCustomer = True
            customer1 = Customer.objects.get(user = user)
            order = OrderItem.objects.filter(order__customer=customer1).order_by('-created')
            context = {'data': customer1 ,'order':order, 'customer':CheckCustomer}
            return render(request,'dashboard.html',context)

        else:
            CheckCustomer = False
            vendor = Customer.objects.get(user = user)
            products = Product.objects.filter(vendor=vendor).order_by('-created')
            context = {'data':vendor,'customer':CheckCustomer , 'products':products}
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

        request.session['product'] = product.id
        request.session['quantity'] = quantity
        request.session['total']= int(product.price) * int(quantity)
        return HttpResponseRedirect('/cart/')

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
            product = Product.objects.get(id=request.session['product'])
            return render(request,'cart.html', {'product':product,})
        except KeyError:
            return render(request,'cart.html', { })
    def post(self,request):
            return HttpResponseRedirect('/checkout/')

class CheckoutView(LoginRequiredMixin,TemplateView):
    template_name = 'checkout.html'
    login_url = '/login/'

    def get(self, request):
        added = False
        try:
            product = Product.objects.get(id=request.session['product'])
            customer = Customer.objects.get(user = request.user)
            context = {'customer':customer}
        except:
            context ={'NoCart':True}
        return render(request,'checkout.html',context)

    def post(self,request):
        order = Order(customer=request.user.customer)
        order.save()
        orderitem = OrderItem(order = order)
        orderitem.product = Product.objects.get(id=request.session['product'])
        orderitem.quantity= request.session['quantity']
        orderitem.price = request.session['total']
        orderitem.save()
        del request.session['product']
        del request.session['quantity']
        del request.session['total']

        added = True
        return render(request,'checkout.html',{'added':added})