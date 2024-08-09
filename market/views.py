from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View


def index(request):
    context = {}
    return render(request, 'market/index.html', context)
