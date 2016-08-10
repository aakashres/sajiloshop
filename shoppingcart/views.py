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
    context = {'product': product}
    return render(request,'index.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def update(request, pk=None):
    user = User.objects.get(pk=pk)
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

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get(self, request):
        user = self.request.user
        customer1 = Customer.objects.filter(user = user)
        vendor = Vendor.objects.filter(user = user)

        if customer1:
            customerYes = True
            order1 = OrderItem.objects.filter(order=Order.objects.filter(customer = customer1))
            context = {'data': customer1 , 'order':order1, 'customer':customerYes}
            return render(request,'dashboard.html',context)

        else:
            customerYes = False
            products = Product.objects.filter(vendor=vendor).order_by('-created')
            context = {'data':vendor,'customer':customerYes , 'products':products}
            return render(request,'dashboard.html',context)


class AddProductView(TemplateView):
    template_name = "addproduct.html"
    model = Product

    def post(self,request):
        added = False
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
        return render_to_response('addproduct.html',{'added':added})

    def get(self, request):
        category = Category.objects.all()
        return render(request,'addproduct.html',{'category':category})







