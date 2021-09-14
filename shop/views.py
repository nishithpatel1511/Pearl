from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt

from .models import Product, customer, Pearl_Users
from math import ceil

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
    for i in list(prod.values('ProductColor')):
        img_list = []
        cur = conn.execute(f'''SELECT image FROM shop_productcolorimages WHERE colour_id = {i['ProductColor']}''')
        for j in cur:
            img_list.append(j[0])
        all_images.append(img_list)
    conn.close()
    ram = {}
    rom = {}
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
        add = Pearl_Users(firstname=i['firstname'], lastname=i['lastname'], username=i['username'],
            password=i['password'], dateofbirth=i['date_of_birth'], country=i['country'],
            mobile= (i['country-code']+i['mobile']), email= i['email'])
        add.save()
    return render(request, 'shop/signup.html')

def username_validation(request):
    uname = request.GET['e_username']
    for i in Pearl_Users.objects.values('username'):
        if uname == i['username']:
            return HttpResponse("taken")
    return HttpResponse("available")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        i = request.POST
        try:
            user_info = Pearl_Users.objects.filter(username = i['username_login'], password = i['password_login'])[0]
            return HttpResponse('valid')
        except:
            return HttpResponse('invalid')
            
    return HttpResponse("invalid")
       
@csrf_exempt
def ajax_email_signup(request):
    if request.method == 'POST':
        i = request.POST
        try:
            user_email = Pearl_Users.objects.filter(email = i['email_signup'])[0]
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


def temp(request):
    return render(request, 'shop/temp.html')
