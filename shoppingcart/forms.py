from shoppingcart.models import PersonalInfo, Customer, Vendor
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    email= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password','first_name','last_name')


class CustomerForm(forms.ModelForm):

    dob= forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    address= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ('dob','address','phone','email',)

class VendorForm(forms.ModelForm):

    dob= forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    address= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Vendor
        fields = ('dob','address','phone','email','description')