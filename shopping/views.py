from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


from carton.cart import Cart
from products.models import Product


def add(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.add(product, price=product.price)
    return redirect('shopping-cart-show')


def remove(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.remove(product)
    return redirect('shopping-cart-show')


def show(request):
    return render(request, 'shopping/show-cart.html')
