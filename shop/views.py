

from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from .models import Product, Pearl_Users, myCart, myCartItem, myCategoryVariant, myProduct, myProductVariantValue
from math import ceil
from django.urls import reverse


import sqlite3


def index(request):
    allprods =[]
    catprods = Product.objects.values('category', 'id')
    cats = sorted({item['category'] for item in catprods}) 
    for cat in cats:
        prod = Product.objects.filter(category=cat)
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


def productView(request, id):

    prod = Product.objects.filter(id=id)
    conn = sqlite3.connect('db.sqlite3')
    all_images= []
    if prod[0].has_color:
        for i in list(prod.values('ProductColor')):
            img_list = []
            cur = conn.execute(f'''SELECT image FROM shop_productcolorimages WHERE colour_id = {i['ProductColor']}''')
            for j in cur:
                img_list.append(j[0])
            all_images.append(img_list)
        conn.close()
    else:
        all_images.append([prod[0].image])
    ram = {}
    rom = {}
    if prod[0].has_storage:
        for i in prod[0].ProductMemoryRom.all():
            rom[i.rom] = {"price": i.price_diff, "mrp": i.mrp_diff}
        for i in prod[0].ProductMemoryRam.all():
            ram[i.ram] = {"price": i.price_diff, "mrp": i.mrp_diff}
    params = {'product': prod, 'product_images': all_images, 'ram': ram, 'rom': rom}
    return render(request, 'shop/productview.html', params)

def search(request):
    return HttpResponse("Search")

def checkout(request):
    return HttpResponse("check out")

def signup(request):
    if request.method == "POST":
        i =request.POST
        add = Pearl_Users(first_name=i['firstname'], last_name=i['lastname'], username=i['username'],
            password=make_password(i['password']), date_of_birth=i['date_of_birth'], country=i['country'],
            mobile= (i['country-code']+i['mobile']), email= i['email'])
        add.save()
    return render(request, 'shop/signup.html')

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
            user_mobile = Pearl_Users.objects.filter(mobile = i['mobile_signup'])[0]
            return HttpResponse("invalid")
        except:
            return HttpResponse("valid")

def temp(request,slug):
    product = myProduct.objects.get(slug = slug)
    product = {'product':product}
    return render(request, 'shop/temp.html', product)


def temphome(request):
    allProduct = myProduct.objects.all()
    n= len(allProduct)
    n2 = n // 2 + ceil((n / 2) - n // 2)
    n = n // 4 + ceil((n / 4) - n // 4)
    allProduct  = {'allProduct': allProduct, 'range4':range(1,n), 'range2':range(1,n2), 'n':n}
    return render(request, 'shop/temphome.html', allProduct)

def myCartView(request):
    if request.user.is_authenticated:
        try:
            cart = myCart.objects.get(user = request.user)
        except:
            cart = myCart.objects.create(user = request.user)
        cart = {'cart':cart}
        return render(request, 'shop/tempcart.html', cart)
    else:
        return HttpResponseRedirect(reverse('signup'))

def updateMyCart(request, slug):
    if request.user.is_authenticated:
        try:
            qty = request.GET.get('qty')
            update_qty = True
        except:
            qty = 1
            update_qty = False

       
            
        try:
            cart = myCart.objects.get(user = request.user)
        except:
            cart = myCart.objects.create(user = request.user)
        try:
            product = myProduct.objects.get(slug = slug)
            cart_item, created = myCartItem.objects.get_or_create(cart = cart, product = product)
            notes = {}
            try:
                for variant in product.product_variant.all():
                    if (variant.unit) != None and variant.unit != 'None':
                        notes[str(variant)] = variant.unit
                    else:
                        notes[str(variant)] = ''
                    # notes[str(variant)] = request.GET.get(str(variant))
                    notes[str(variant)] = str(myProductVariantValue.objects.get(id = request.GET.get(str(variant)))) + notes[str(variant)]
            except:
                notes['color'] = None
            
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
            for item in cart.my_cart.all():
                new_total += (item.product.price * item.quantity)
            cart.total = new_total
            cart.save()
            return HttpResponseRedirect(reverse('mycart'))
        except:
            return HttpResponse("None")
    
    else:
        return HttpResponse('Not Logged In')

def myCategoryOption(request):
    options = '<option value="" selected>---------</option>'
    try:
        cat = request.GET.get('selected_category_id')
        optn = myCategoryVariant.objects.filter(category = cat)
        for item in optn:
            options += f'<option value="{item.id}">{item}</option>' 
        return HttpResponse(options)
    except:
        return HttpResponse(options)
