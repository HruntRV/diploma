from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login', LoginView.as_view(template_name='market/login.html'), name='market_login'),
    path('logout', LogoutView.as_view(), name='market_logout'),
    path('registration', views.registration, name='registration'),
    path('registration_success', views.registration_success, name='registration_success'),
    path('profile/', views.profile, name='profile')

    ]
