

from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

# from .models import Product, Pearl_Users, Cart, CartItem, CategoryVariant, Product, ProductColor, ProductVariantValue
from .models import *
from math import ceil
from django.urls import reverse


def index(request):
    allprods =[]
    categorys = Category.objects.all()
    for cat in categorys:
        prod = Product.objects.filter(category=cat.id)
        n = len(prod)
        n2 = n // 2 + ceil((n / 2) - n // 2)
        n = n // 4 + ceil((n / 4) - n // 4)
        r2 = range(1, n2)
        allprods.append([prod, range(1,n), r2, n])
    params = {'allprods': allprods}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def tracker(request):
    return HttpResponse("tracker")

def productView(request,slug):
    product = Product.objects.get(slug = slug)
    product = {'product':product}
    return render(request, 'shop/productview.html', product)

def search(request):
    return HttpResponse("Search")

def checkout(request):
    return HttpResponse("check out")

def signup(request):
    if request.method == "POST":
        i =request.POST
        add = Pearl_Users(first_name=i['firstname'], last_name=i['lastname'], username=i['username'],
            password=make_password(i['password']), date_of_birth=i['date_of_birth'], country=Country.objects.get(id = i['country']).country_name,
            mobile= (Country.objects.get(id = i['country-code']).country_code+i['mobile']), email= i['email'])
        add.save()
    
    return render(request, 'shop/signup.html', {'country': Country.objects.all()})

def username_validation(request):
    try:
        uname = Pearl_Users.objects.filter(username=request.GET['e_username'])[0]
        return HttpResponse("taken")
    except:
        return HttpResponse("available")

@csrf_exempt
def login_validate(request):

    if request.method == 'POST':
        i = request.POST
        user = authenticate(username=i['username_login'], password=i['password_login'])
        if user is not None:
            login(request, user)
            return HttpResponse("valid")
        else:
            return HttpResponse("invalid")
    else:
        return HttpResponse("404-Page Not Found")

def login_page(request):
    return render(request, 'shop/login.html')

def logout_validate(request):
    try:
        logout(request)
        return HttpResponse("logout")
    except:
        return HttpResponse("error")
       
@csrf_exempt
def ajax_email_signup(request):
    if request.method == 'POST':
        i = request.POST
        try:
            user_email = Pearl_Users.objects.filter(email=i['email_signup'])[0]
            return HttpResponse("invalid")
        except:    
            return HttpResponse("valid")
            
@csrf_exempt
def ajax_mobile_signup(request):
    if request.method == "POST":
        i = request.POST
        try:
            cd = Country.objects.get(id = i['mobile_signup'].split()[0]).country_code
            user_mobile = Pearl_Users.objects.get(mobile = cd+i['mobile_signup'].split()[1])
            return HttpResponse("invalid")
        except:
            return HttpResponse("valid")

def temp(request,slug):
    product = Product.objects.get(slug = slug)
    product = {'product':product}
    return render(request, 'shop/temp.html', product)

def CartView(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user = request.user)
        except:
            cart = Cart.objects.create(user = request.user)
        cart = {'cart':cart}
        return render(request, 'shop/cart.html', cart)
    else:
        return HttpResponseRedirect(reverse('loginpage'))

def updateCart(request, slug):
    if request.user.is_authenticated:
        try:
            qty = request.GET.get('qty')
            update_qty = True
        except:
            qty = 1
            update_qty = False
        try:
            cart = Cart.objects.get(user = request.user)
        except:
            cart = Cart.objects.create(user = request.user)
        try:
            product = Product.objects.get(slug = slug)
            try:
                itm = request.GET.get('item')
                cart_item = CartItem.objects.get(pk = itm)
            except:
                notes = '('
                if product.has_colour_option:
                    notes += (str(ProductColor.objects.get(id = str(request.GET.get('color')).split('_')[1])) + ", ")
                for variant in product.product_variant.all():
                    
                    if (variant.unit) != None and variant.unit != 'None':
                        notes += (str(ProductVariantValue.objects.get(id = request.GET.get(str(variant)))) + f"{variant.unit}, ")
                        # notes[str(variant)] = variant.unit
                    else:
                        notes += (str(ProductVariantValue.objects.get(id = request.GET.get(str(variant)))) + ", ")
                    # notes[str(variant)] = str(ProductVariantValue.objects.get(id = request.GET.get(str(variant)))) + notes[str(variant)]
                notes = notes[:-2]+')'
                cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product, notes = notes)
                
                if created:
                    for variant in product.product_variant.all():
                        CartItemVariant.objects.create(item = cart_item, variant = ProductVariantValue.objects.get(id = request.GET.get(str(variant))))
                    if product.has_colour_option:
                        CartItemColor.objects.create(item = cart_item, color = ProductColor.objects.get(id = str(request.GET.get('color')).split('_')[1]))
                        

            if int(qty) == 0 and update_qty:
                cart_item.delete()
                # cart.my_cart.remove(cart_item)
            elif update_qty:
                cart_item.quantity = qty
                cart_item.notes = notes
                cart_item.save()
            else:
                pass
            
            new_total = 0
            for item in cart.cart_items.all():
                new_total += (item.product.price * item.quantity)
            cart.total = new_total
            cart.save()
            return HttpResponseRedirect(reverse('cart'))
        except:
            return HttpResponse("None")
    
    else:
        return render(request, 'shop/login.html')

def productImages(request):
    try:
        id = request.GET.get('color')
        color = ProductColor.objects.get(id=id)
        rs = f'<ul class="product-view-image-list" id="color_{id}_images">'
        ctrl = ''
        cnt = 1
        for image in color.color_images.all():
            if cnt == 1:
                ctrl += f'<button type="button" class="my-sliderbuttons active" id="ctrl_btn_{cnt}"></button>'
            else:
                ctrl += f'<button type="button" class="my-sliderbuttons" id="ctrl_btn_{cnt}"></button>'
            rs += f'<li class="small-image-li"> <img src="/media/{image.image}"></li>'
            cnt += 1
        rs += '</ul>'
        return HttpResponse(rs+'\n'+ctrl)
    except:
        return HttpResponse('')

