from django.shortcuts import render, redirect

from .models import *


def home(request):
    products = Product.objects.all()

    data = {
        'products': products,
    }

    return render(request, 'main/home.html', data)


def product_info(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        try:
            cp = CartProduct.objects.get(cart__user=request.user, product=product, cart__is_bought=False)
            cp.count += 1
            cp.save()

            return redirect('product', product_id)
        except CartProduct.DoesNotExist:
            cp = CartProduct.objects.create(product=product, count=1)
            cp.save()

            cart = Cart.objects.get(user=request.user, is_bought=False)
            cart.cart_products.add(cp)
            cart.save()

            return redirect('product', product_id)

    data = {
        'product': product,
    }

    return render(request, 'main/product.html', data)
