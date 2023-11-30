from django.contrib.auth.models import User

from .models import Cart


def add_variable_to_context(request):
    if not request.user.is_authenticated:
        data = {
            'cart_price': 0
        }

        return data

    try:
        cart = Cart.objects.get(user=request.user, is_bought=False)
        data = {
            'cart_price': cart.total_price
        }
    except Cart.DoesNotExist:
        data = {
            'cart_price': 0
        }

    return data
