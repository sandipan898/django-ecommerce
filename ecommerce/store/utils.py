from . models import *
import json


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('cart:', cart)
    order_items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_total']

    for i in cart:
        try:
            cart_items += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            order_item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                }, 
                'quantity': cart[i]["quantity"],
                'get_total': total,
            }
            order_items.append(order_item)     

            if product.digital == False:
                order['shipping'] = True       
        
        except:
            pass

    return {'cart_items': cart_items, 'order': order, 'order_items': order_items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all() # get all the orderitem that has that order as parent
        cart_items = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cart_items = cookieData['cart_items']
        order = cookieData['order']
        order_items = cookieData['order_items']

    return {'cart_items': cart_items, 'order': order, 'order_items': order_items}


def guest_order(request, data):
    print('User is not logged in')
    print("COOKIES:", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    order_items = cookieData['order_items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in order_items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return order, customer