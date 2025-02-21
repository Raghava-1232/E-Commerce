from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def get_cart_total(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            return order.get_cart_items
        except:
            return 0
    return 0

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    cart_total = get_cart_total(request)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            Customer.objects.create(
                user=user,
                name=username,
                email=email
            )
            messages.success(request, 'Account created successfully')
            return redirect('login')
        except:
            messages.error(request, 'Error creating account')
            
    return render(request, 'store/register.html')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({
        'itemQuantity': orderItem.quantity if orderItem.quantity > 0 else 0,
        'itemTotal': float(orderItem.get_total) if orderItem.quantity > 0 else 0,
        'cartItems': order.get_cart_items,
        'cartTotal': float(order.get_cart_total)
    })

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'store/product.html', context)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])

        if total == float(order.get_cart_total):
            order.complete = True
        order.transaction_id = transaction_id
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in..')

    return JsonResponse('Payment submitted..', safe=False)

@login_required(login_url='login')
def order_history(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(
            customer=customer, 
            complete=True
        ).order_by('-date_ordered')
        context = {'orders': orders}
        return render(request, 'store/orders.html', context)

def reset_password(request):
    return render(request, 'store/reset_password.html')

def product_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        
    context = {
        'product': product,
        'cartItems': cartItems
    }
    return render(request, 'store/product_detail.html', context)