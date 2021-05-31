from django.shortcuts import render
from.models import *
from django.http import JsonResponse
import json

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created =  Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        order_items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}  
        cart_items = order['get_cart_total']

    products = Product.objects.all()
    context = { "products": products, 'cart_items': cart_items }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all() # get all the orderitem that has that order as parent
        cart_items = order.get_cart_items
    else:
        order_items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_total']

    context = {'items': order_items, 'order': order, 'cart_items': cart_items }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all() # get all the orderitem that has that order as parent
        cart_items = order.get_cart_items
    else:
        order_items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_total']

    context = {'items': order_items, 'order': order, 'cart_items': cart_items }
    return render(request, 'store/checkout.html', context)
            
def update_item(request):
    data = json.loads(request.body)
    print(request.body)
    product_id = data['productId']
    action = data['action']
    print('Product:', product_id)
    print('Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add': 
        order_item.quantity += 1
    elif action == 'remove': 
        order_item.quantity -= 1
    
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item is added', safe=False)
