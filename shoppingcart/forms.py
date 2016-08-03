from shoppingcart.models import PersonalInfo
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class PersonalInfoForm(forms.ModelForm):

    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob= forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PersonalInfo
        fields = ('first_name','last_name','dob','address','phone','email')
