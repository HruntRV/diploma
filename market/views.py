from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View

from .forms import ProductFilterForm
from .models import Profile, Category, Product, ProductCharacteristicValue
from django.db.models import Q
from cart.forms import CartAddProductForm
from market.models import Product, Category


def index(request):
    context = {}
    return render(request, 'market/index.html', context)


@login_required
def profile(request):
    profile_data = get_object_or_404(Profile, user=request.user)
    context = {'profile_data': profile_data}
    return render(request, 'market/profile.html', context)


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                new_profile = Profile(user=new_user, phone=phone)
                new_profile.save()
                login(request, new_user)  # Automatically log the user in
                return redirect('registration_success')  # Redirect to success page
            else:
                return HttpResponse("User with this username or email already exists", status=400)
        else:
            return HttpResponse("Passwords do not match", status=400)

    return render(request, 'registration.html')


def registration_success(request):
    context = {}
    return render(request, 'market/registration_success.html', context)


def my_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('market:index')  # Redirect to the profile page or any other page
        else:
            return HttpResponse("Invalid email or password", status=400)

    return render(request, 'market/login.html')


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request,
#                   'market/product/list.html',
#                   {'category': category,
#                    'categories': categories,
#                    'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    characteristic_values = ProductCharacteristicValue.objects.filter(product=product)

    return render(request,
                  'market/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form, 'characteristic_values': characteristic_values})


def search(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(
            Q(category__name__icontains=query) |
            Q(name__icontains=query) |
            Q(slug__icontains=query)
        )
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'market/product/list.html', context)


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    categories = Category.objects.all()

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    form = ProductFilterForm(category=category)

    if request.GET:
        form = ProductFilterForm(request.GET, category=category)
        if form.is_valid():
            for field, value in form.cleaned_data.items():
                if field.startswith('char_') and value:
                    char_id = field.split('_')[1]
                    products = products.filter(characteristic_values__characteristic_id=char_id,
                                               characteristic_values__value=value)

    return render(request, 'market/product/list.html',
                  {'category': category, 'categories': categories, 'products': products, 'form': form})


def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category__in=category.get_descendants(include_self=True))
    categories = Category.objects.all()  # Retrieve all categories
    return render(request, 'market/product/list.html', {'category': category, 'products': products, 'categories': categories})


def categories_list(request):
    return render(request, 'market/product/categories_list.html')
