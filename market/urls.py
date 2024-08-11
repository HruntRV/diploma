from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .import views
# from .views import MyLogoutView


urlpatterns = [
    path('', views.index, name="index")
    ]
