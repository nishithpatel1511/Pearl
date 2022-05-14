
from time import time, sleep
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
import sqlite3
from django.utils.timezone import now

conn = sqlite3.connect('db.sqlite3')

product_category = (
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Home', 'Home'),
)

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=product_category)
    subcategory = models.CharField(max_length=50, default="")
    image = models.ImageField(default="")
    pub_date = models.DateField()
    base_price = models.IntegerField(default=0)
    base_mrp = models.IntegerField(default=0)
    base_ram = models.IntegerField(default=0)
    has_storage = models.BooleanField(default="False")
    display_ram = models.BooleanField(default="False")
    has_color = models.BooleanField(default="False")
    def __str__(self):
        return self.product_name
class ProductImages(models.Model):
    product =models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ProductImages')
    image = models.ImageField(default="")
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
    user_permissions = None
    groups = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country', 'mobile', 'email', 'date_of_birth']

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username


class myCategory(models.Model):
    category_name = models.CharField(max_length=30)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    update = models.DateField(auto_now=True, auto_now_add=False)
    def __str__(self) -> str:
        return self.category_name

class myCategoryVariant(models.Model):
    category = models.ForeignKey(myCategory, related_name='mycategory', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=30)
    variant_unit = models.CharField(max_length=20, default='')
    def __str__(self) -> str:
        return self.variant_name

class myProduct(models.Model):
    product_name = models.CharField(max_length=20)
    # category = models.OneToOneField(myCategory,on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(myCategory, on_delete=models.CASCADE, related_name='myproductcategory', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(default='')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    def __str__(self) -> str:
        return self.product_name
    def get_absolute_url(self):
        return reverse('temp', kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):
        if self.pk != None and myProduct.objects.get(pk = self.pk).category != self.category:
            print(myProductVariant.objects.filter(product = self.pk).delete())
            super().save(*args, **kwargs, update_fields=['category'])
        else:
            super().save(*args, **kwargs)
        
    class Meta:
        unique_together = ('product_name', 'slug')

class myProductVariant(models.Model):
    product = models.ForeignKey(myProduct, on_delete=models.CASCADE, related_name='product_variant')
    variant_type = models.ForeignKey(myCategoryVariant, on_delete=models.CASCADE)
    unit = models.CharField(max_length=20, default='', null=True, blank=True)
    def __str__(self) -> str:
        return str(self.variant_type)
    class Meta:
        unique_together = (('product', 'variant_type'))
class myProductVariantValue(models.Model):
    variant_type = models.ForeignKey(myProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name='variant_value')
    value = models.CharField(max_length=25)
    def __str__(self) -> str:
        return self.value

class myCart(models.Model):
    user = models.OneToOneField(Pearl_Users, on_delete= models.CASCADE, related_name='user', null=False, blank=False, default=None)
    # items = models.ManyToManyField(myCartItem, null=True, blank=True)
    # products = models.ManyToManyField(myProduct, null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    timestamp = models.TimeField(auto_now = False, auto_now_add=True)
    updated = models.DateTimeField(auto_now = True, auto_now_add=False)
    def __str__(self) -> str:
        return self.user.username

class myCartItem(models.Model):
    cart = models.ForeignKey(myCart, on_delete = models.CASCADE, related_name='my_cart', blank=True, null=True)
    product = models.ForeignKey(myProduct, on_delete=models.CASCADE, related_name='myproduct')
    quantity = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self) -> str:
        return self.product.product_name

MY_CATEGORIES = {
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package')
}

class myVariance(models.Model):
    product = models.ForeignKey(myProduct, on_delete=models.CASCADE, related_name='myproduct_variance')
    category = models.CharField(max_length=25, choices=MY_CATEGORIES, default='size')
    title = models.CharField(max_length=100)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=100)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self) -> str:
        return self.title
