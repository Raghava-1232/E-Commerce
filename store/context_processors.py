from .models import Order, Customer

def cart_total(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            return {'cart_total': order.get_cart_items}
        except:
            return {'cart_total': 0}
    return {'cart_total': 0} 