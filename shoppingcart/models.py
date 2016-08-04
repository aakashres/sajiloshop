from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
#import datetime

# Create your models here.

class PersonalInfo(models.Model):

    user = models.OneToOneField(User)
    dob = models.DateField(null=True, blank=True )
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True

class TimeStamp(models.Model):

    created = models.DateTimeField(default= timezone.now,null=True)
    modified = models.DateTimeField(default= timezone.now,null=True)

    class Meta:
        abstract = True

class Customer(PersonalInfo, TimeStamp):

    cart = models.TextField()
    STATUS_CHOICES = (
        (1, 'Verified'),
        (2, 'Not Verified'))
    status = models.IntegerField( choices = STATUS_CHOICES, default= 0 )

    def __str__(self):
        return self.user.username

class Vendor(PersonalInfo):

    description = models.CharField(max_length=80)
    STATUS_CHOICES = (
        (1, 'Verified'),
        (2, 'Not Verified'))
    status = models.IntegerField( choices = STATUS_CHOICES, default= 0 )


class Category(TimeStamp):

    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    parent = models.ForeignKey('self' , null=True,blank=True)

    def __str__(self):
        return self.category_name


class Product(TimeStamp):

    product_name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    feature = models.TextField()
    vendor = models.ForeignKey(Vendor)
    tags = models.TextField()
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.product_name

class Order(TimeStamp):
    customer = models.ForeignKey(Customer)

class OrderItem(TimeStamp):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    price = models.IntegerField()