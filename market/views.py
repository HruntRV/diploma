from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.views import View

from .forms import ProductFilterForm, CommentForm, QuestionForm, UpdateForm
from .models import Profile, Category, Product, ProductCharacteristicValue, Comment, Question, WishList
from django.db.models import Q
from cart.forms import CartAddProductForm
from market.models import Product, Category
from django.conf import settings


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # User's name
        user_email = request.POST.get('email')  # User's email address
        message = request.POST.get('message')  # User's message

        # Compose the email to yourself
        subject = f"Contact form submission from {name}"
        message_body = f"Name: {name}\nEmail: {user_email}\n\nMessage:\n{message}"

        # Send the email to yourself
        send_mail(
            subject,
            message_body,
            user_email,  # From: user's email address
            [settings.DEFAULT_FROM_EMAIL],  # To: your email address (elerom.dp@gmail.com)
            fail_silently=False,
        )
        confirmation_subject = "Thank you for contacting us"
        confirmation_message = f"Hi {name},\n\nThank you for reaching out. We have received your message and will get back to you soon."

        send_mail(
            confirmation_subject,
            confirmation_message,
            settings.DEFAULT_FROM_EMAIL,  # From: your email address (elerom.dp@gmail.com)
            [user_email],  # To: user's email address
            fail_silently=False,
        )

        return HttpResponse("Thank you for your message. We will get back to you soon.")

    return render(request, 'market/contact.html')


def home(request):
    products = Product.objects.all()
    return render(request, 'market/home.html', {'products': products})


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
            return redirect('market:home')
        else:
            return HttpResponse("Invalid email or password", status=400)

    return render(request, 'market/home.html')


def product_detail(request, id, slug):
    # wishlist = None
    in_wishlist = False
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    # wish_list_product = Product.objects.all()
    user = request.user
    if user.is_authenticated:
        wishlist = WishList.objects.filter(user=user).first()
        in_wishlist = wishlist and wishlist.products.filter(id=product.id).exists()

    comments = Comment.objects.filter(product=product).order_by('-published_date')
    questions = Question.objects.filter(product=product).order_by('-published_date')
    if request.method == 'POST':
        if 'comment_form' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.author = request.user.profile
                comment.save()
                return redirect('market:product_detail', id=product.id, slug=product.slug)
        elif 'question_form' in request.POST:
            qform = QuestionForm(request.POST)
            if qform.is_valid():
                question = qform.save(commit=False)
                question.product = product
                question.author = request.user.profile
                question.save()
                return redirect('market:product_detail', id=product.id, slug=product.slug)
    else:
        form = CommentForm()
        qform = QuestionForm()

    cart_product_form = CartAddProductForm()
    characteristic_values = ProductCharacteristicValue.objects.filter(product=product)

    context = {
        'characteristic_values': characteristic_values,
        'cart_product_form': cart_product_form,
        'product': product,
        'comments': comments,
        'questions': questions,
        'form': form,
        'qform': qform,
        'in_wishlist': in_wishlist
    }
    return render(request, 'market/product/detail.html', context)


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


def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            profile.gender = form.cleaned_data['Gender']
            profile.phone = form.cleaned_data['Phone']
            profile.country = form.cleaned_data['Country']
            profile.city = form.cleaned_data['City']
            profile.avatar = form.cleaned_data['Avatar']
            profile.save()

            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
                user.save()
                update_session_auth_hash(request, user)

            return redirect('market:profile')
    else:
        initial_data = {
            'Gender': profile.gender,
            'Phone': profile.phone,
            'Country': profile.country,
            'City': profile.city,
        }
        form = UpdateForm(instance=user, initial=initial_data)

        context = {'form': form}
        return render(request, "market/update_profile.html", context)


def wishlist(request):
    user = request.user
    wishlist = get_object_or_404(WishList, user=user)
    products = wishlist.products.all()
    context = {'products': products}
    return render(request, "market/product/list.html", context)


# def add_to_wishlist(request, product_id):
#     if request.user.is_authenticated:
#         product = get_object_or_404(Product, id=product_id)
#         wishlist, created = WishList.objects.get_or_create(user=request.user)
#         if product not in wishlist.products.all():
#             wishlist.products.add(product)
#             return JsonResponse({'status': 'added'}, status=200)
#         else:
#             wishlist.products.remove(product)
#             return JsonResponse({'status': 'removed'}, status=200)
#     return JsonResponse({'status': 'not_authenticated'}, status=403)
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)

    if wishlist.products.filter(id=product.id).exists():
        wishlist.products.remove(product)
        status = 'removed'
    else:
        wishlist.products.add(product)
        status = 'added'

    return JsonResponse({'status': status})



