from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,CreateUserForm,Customer_profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group


# Create your views here.
@login_required(login_url='login')
def customer(request,id):
    customers=Customer.objects.get(id=id)
    
    orders = customers.order_set.all()
    order_count=orders.count()
    return render(request,'customer.html',{'customers':customers,'orders':orders,'order_count':order_count})

@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_orders=orders.count()
    delivered=Order.objects.filter(status="Delivered").count()
    pending=Order.objects.filter(status='pending').count()
    return render(request,'home.html',{'total_orders':total_orders,'delivered':delivered,'pending':pending,'customers':customers,'orders':orders})


def main(request):
    return render(request,'main.html')


@login_required(login_url='login')   
@allowed_users(allowed_roles=["admin"]) 
def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request):
    form=OrderForm()
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'create_order.html',{'form':form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,id):
    orders=Order.objects.get(id=id)
    form=OrderForm(instance=orders)
    if request.method=='POST':
        form=OrderForm(request.POST,instance=orders)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    return render(request,'create_order.html',{'form':form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,id):
    orders=Order.objects.get(id=id)
    if request.method=='POST':
        orders.delete()
        return redirect('home')
        
    return render(request,'delete.html',{'orders':orders})

@unauthenticated_user
def RegisterPage(request):
    
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username
            )
            messages.success(request,"User is created")
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)
    
@unauthenticated_user
def loginPage(request):
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.info(request,"Incorrect Username or Password")

    context={}
    return render(request,'login.html',context)


def logoutPage(request):
    context={}
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    pending=orders.filter(status='pending').count()
    delivered=orders.filter(status='Delivered').count()
    context={'orders':orders,'total_orders':total_orders,'pending':pending,'delivered':delivered}
    return render(request,'user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def settings_profile(request):
    customer=request.user.customer
    form=Customer_profile(instance=customer)
    if request.method=='POST':
        form=Customer_profile(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}

    return render (request,'settings.html',context)