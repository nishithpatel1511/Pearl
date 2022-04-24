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
    path('uname/', views.username_validation, name= "unamevalidation"),
    path('login/', views.login_validate, name="login"),
    path('logout/', views.logout_validate, name="logout"),
    path('ajax_email_signup/', views.ajax_email_signup, name="ajax_email_signup"),
    path('ajax_mobile_signup/', views.ajax_mobile_signup, name="ajax_mobile_signup"),

    path('myproduct/<slug>/', views.temp, name = 'temp'),
    path('myproducts/', views.temphome, name = 'myproducts'),
    path('mycart/', views.myCartView, name='mycart'),
    path('mycart/<slug>/', views.updateMyCart, name='mycartupdate'),
    path('ajaxProductSubcategory/', views.myCategoryOption, name="getProductSubcategory"),

]