from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime

from .forms import Authenticate, CreateUserForm
from main.models import Order, Cart, CartProduct


@login_required(login_url='login')
def account_home(request):
    orders = Order.objects.filter(user=request.user)
    products_list = [CartProduct.objects.filter(cart__order=order) for order in orders]

    combined_data = [{'order': order, 'products': products} for order, products in zip(orders[::-1], products_list[::-1])]

    data = {
        'combined_data': combined_data
    }

    return render(request, 'account/account_home.html', data)


def register(request):
    if request.user.is_authenticated:
        return redirect('account')
    else:
        error = ''
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()

                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)

                login(request, user)
                Cart.objects.create(user=user)

                return redirect('home')
            else:
                error = 'Неправильно введенные данные'

        data = {
            'form': form,
            'error': error
        }

        return render(request, 'account/register.html', data)


def login_acc(request):
    if request.user.is_authenticated:
        return redirect('account')
    else:
        error = ''
        form = Authenticate()

        if request.method == 'POST':
            form = Authenticate(data=request.POST)

            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(username=username, password=password)
                try:
                    Cart.objects.get(user=user, is_bought=False)
                except Cart.DoesNotExist:
                    Cart.objects.create(user=user)

                if user is not None:
                    login(request, user)
                    return redirect('account')
            else:
                error = 'Неправильно введенные данные'
        data = {
            'form': form,
            'error': error,
        }

    return render(request, 'account/login.html', data)


@login_required(login_url='login')
def logout_acc(request):
    if request.user.is_authenticated:
        logout(request)

        return redirect('home')


@login_required(login_url='login')
def basket(request):
    try:
        cart = Cart.objects.get(user=request.user, is_bought=False)
    except Cart.DoesNotExist:
        cart = None

    products = CartProduct.objects.filter(cart=cart)

    if request.method == 'POST' and len(request.POST) == 2:
        prod_id, operand = list(dict(request.POST).keys())[1].split()
        prod_id = int(prod_id)

        prod = cart.cart_products.get(id=prod_id)
        if operand == '+':
            prod.count += 1
            prod.save()
        else:
            prod.count -= 1
            prod.save()
            if prod.count <= 0:
                cart.cart_products.remove(prod)
                prod.delete()

    if request.method == 'POST' and len(request.POST) == 1:
        cart.is_bought = True
        cart.save()
        Cart.objects.create(user=request.user)
        order = Order.objects.create(user=request.user, cart=cart, date=datetime.date.today())
        order.save()

        return redirect('basket')

    data = {
        'cart': cart,
        'products': products
    }

    return render(request, 'account/basket.html', data)
