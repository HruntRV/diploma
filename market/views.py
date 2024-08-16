from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from .models import Profile


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

