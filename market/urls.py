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
    path('categories_list', views.categories_list, name='categories_list'),
    path('products', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('search', views.search, name='search'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist')

    ]
