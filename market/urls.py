from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.my_login, name='market_login'),
    path('logout', LogoutView.as_view(), name='market_logout'),
    path('registration', views.registration, name='registration'),
    path('registration_success', views.registration_success, name='registration_success'),
    path('profile/', views.profile, name='profile'),
    path('market', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('search', views.search, name='search')

    ]
