from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('product/<slug>/', views.productView, name="product"),
    path('product_images/', views.productImages),
    path('cart/', views.CartView, name='cart'),
    path('cart/<slug>/', views.updateCart, name='cartupdate'),
    path('checkout/', views.checkout, name="Checkout"),
    path('search/', views.search, name="Search"),
    path('signup/', views.signup, name="signup"),
    path('uname/', views.username_validation, name= "unamevalidation"),
    path('login/', views.login_validate, name="login"),
    path('loginpage/', views.login_page, name='loginpage'),
    path('logout/', views.logout_validate, name="logout"),
    path('ajax_email_signup/', views.ajax_email_signup, name="ajax_email_signup"),
    path('ajax_mobile_signup/', views.ajax_mobile_signup, name="ajax_mobile_signup"),

    path('temp', views.temp, name = 'temp'),
]