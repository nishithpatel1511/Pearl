from django.contrib.auth.models import AbstractUser
from django.db import models
import sqlite3
from django.utils.timezone import now

conn = sqlite3.connect('db.sqlite3')

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    image = models.ImageField(default="")
    pub_date = models.DateField()
    base_price = models.IntegerField(default=0)
    base_mrp = models.IntegerField(default=0)
    base_ram = models.IntegerField(default=0)
    has_storage = models.BooleanField(default="False")
    display_ram = models.BooleanField(default="False")
    has_color = models.BooleanField(default="True")
    def __str__(self):
        return self.product_name

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name= 'ProductColor')
    color = models.ImageField(default="")

class ProductColorImages(models.Model):
    colour = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name="image_color")
    image = models.ImageField(default="")

class ProductMemoryRom(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name= 'ProductMemoryRom')
    rom = models.IntegerField(default=0)
    price_diff = models.IntegerField(default=0)
    mrp_diff = models.IntegerField(default=0)

class ProductMemoryRam(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ProductMemoryRam')
    ram = models.IntegerField(default=0)
    price_diff = models.IntegerField(default=0)
    mrp_diff = models.IntegerField(default=0)

class Pearl_Users(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(default=now)
    country = models.CharField(max_length=30)
    mobile = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_authenticated = True
    is_anonymous = True
    groups = None
    user_permissions = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country', 'mobile', 'email', 'date_of_birth']

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username
