from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True,blank=True)
    mobileno=models.CharField(max_length=50,null=True,blank=True)
    profile_pic=models.ImageField(default="default.jpg",null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    categories=(
        ('indoor','indoor'),
        ('outdoor','outdoor')
    )

    name=models.CharField(max_length=50,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=50,null=True,choices=categories)
    description=models.CharField(max_length=200,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tag=models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS=(('pending','pending'),
    ('Out for Delivery','Out for Delivery'),
    ('Delivered','Delivered'))

    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    status=models.CharField(max_length=50,choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True)