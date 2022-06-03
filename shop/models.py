
from time import time
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.files.storage import default_storage

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

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    update = models.DateField(auto_now=True, auto_now_add=False)
    def __str__(self) -> str:
        return self.category_name
        
class CategoryVariant(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=30)
    variant_unit = models.CharField(max_length=20, default='')
    def __str__(self) -> str:
        return self.variant_name

class Product(models.Model):
    product_name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    has_colour_option = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(default='')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    def __str__(self) -> str:
        return self.product_name
    def get_absolute_url(self):
        return reverse('product', kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):
        if self.pk != None and Product.objects.get(pk = self.pk).category != self.category:
            ProductVariant.objects.filter(product = self.pk).delete()
            super().save(*args, **kwargs, update_fields=['category'])
        else:
            super().save(*args, **kwargs)
    def delete(self):
        default_storage.delete(self.thumbnail.path)
        if self.has_colour_option:
            for c in self.product_color.all():
                default_storage.delete(c.color_image.path)
                for i in c.color_images.all():
                    default_storage.delete(i.image.path)
        else:
            for i in self.product_images.all():
                default_storage.delete(i.image.path)
        return super().delete()
    class Meta:
        unique_together = ('product_name', 'slug')
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    variant_type = models.ForeignKey(CategoryVariant, on_delete=models.CASCADE)
    unit = models.CharField(max_length=20, default='', null=True, blank=True)
    def __str__(self) -> str:
        return str(self.variant_type)
    def save(self, *args, **kwargs):
        if self.product.category == self.variant_type.category:
            super().save(*args, **kwargs)
    class Meta:
        unique_together = (('product', 'variant_type'))
class ProductVariantValue(models.Model):
    variant_type = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name='variant_value')
    value = models.CharField(max_length=25)
    def __str__(self) -> str:
        return self.value
    def save(self, *args, **kwargs):
        if self.variant_type.product.category == self.variant_type.variant_type.category:
            super().save(*args, **kwargs)

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_color')
    color_name= models.CharField(max_length=30)
    color_image =models.ImageField()
    # show_only_image = models.BooleanField(default=False)
    # show_only_name = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.color_name
class ProductColorImages(models.Model):
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='color_images')
    image = models.ImageField()
    def __str__(self) -> str:
        return str(self.image)
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField()

class Cart(models.Model):
    user = models.OneToOneField(Pearl_Users, on_delete= models.CASCADE, related_name='user_cart', null=False, blank=False, default=None)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    timestamp = models.TimeField(auto_now = False, auto_now_add=True)
    updated = models.DateTimeField(auto_now = True, auto_now_add=False)
    def __str__(self) -> str:
        return self.user.username

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name='cart_items', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self) -> str:
        return f"{self.product.product_name} {self.notes}"

class CartItemVariant(models.Model):
    item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_item_variant')
    variant = models.ForeignKey(ProductVariantValue, on_delete=models.CASCADE, related_name='cart_variant_value')
    def __str__(self) -> str:
        return f"{self.item.product.product_name} ({self.variant.value})"
class CartItemColor(models.Model):
    item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_item_color')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='cart_color_value')
