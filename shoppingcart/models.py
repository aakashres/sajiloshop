from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
#import datetime

# Create your models here.

class PersonalInfo(models.Model):

    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True )
    address = models.CharField(max_length=50)
    phone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True

class TimeStamp(models.Model):

  #  timestamp_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default= timezone.now)
    modified = models.DateTimeField(default= timezone.now)

    class Meta:
        abstract = True

class Customer(PersonalInfo, TimeStamp):

  #  personal_info = models.ForeignKey(PersonalInfo)
    cart = models.TextField(blank=True)
  #  time_stamp = models.ForeignKey(TimeStamp)
    STATUS_CHOICES = (
        (1, 'Verified'),
        (2, 'Not Verified'))
    status = models.IntegerField( choices = STATUS_CHOICES, default= 0 )

class Vendor(PersonalInfo):

 #   personal_info = models.OneToOneField('shoppingcart.PersonalInfo')
 #   time_stamp = models.ForeignKey(TimeStamp)
    description = models.CharField(max_length=50)
    STATUS_CHOICES = (
        (1, 'Verified'),
        (2, 'Not Verified'))
    status = models.IntegerField( choices = STATUS_CHOICES, default= 0 )


class Category(TimeStamp):

    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    parent = models.ForeignKey('self',blank=True, null=True)
    #time_stamp = models.ForeignKey(TimeStamp)

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
   # time_stamp = models.ForeignKey(TimeStamp)

class Order(TimeStamp):

    customer = models.ForeignKey(Customer)
    #time_stamp = models.ForeignKey(TimeStamp)

class OrderItem(TimeStamp):

    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    price = models.IntegerField()
   # time_stamp = models.ForeignKey(TimeStamp)
