from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('productview/<int:id>', views.productView, name="ProductView"),
    path('search/', views.search, name="Search"),
    path('checkout/', views.checkout, name="Checkout"),
    path('signup/', views.signup, name="signup"),
    path('temp/', views.temp, name="temp"),
    path('uname/', views.username_validation, name= "unamevalidation"),
    path('login/', views.login_validate, name="login"),
    path('ajax_email_signup/', views.ajax_email_signup, name="ajax_email_signup"),
    path('ajax_mobile_signup/', views.ajax_mobile_signup, name="ajax_mobile_signup")
]