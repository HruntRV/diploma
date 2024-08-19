from .cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {'cart': cart}

