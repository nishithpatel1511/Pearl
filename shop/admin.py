from django.contrib import admin

from .models import *
import nested_admin

class imageInline(nested_admin.NestedStackedInline):
	model = ProductColorImages
	extra = 0

class colorInline(nested_admin.NestedStackedInline):
	model = ProductColor
	inlines = [imageInline]
	extra = 0

class memoryRomInline(nested_admin.NestedStackedInline):
	model = ProductMemoryRom
	extra = 0

class memoryRamInline(nested_admin.NestedStackedInline):
	model = ProductMemoryRam
	extra = 0

class ProductAdmin(nested_admin.NestedModelAdmin):
	fieldset = [(None, {'fields': ['product_name', 'category', 'subcategory', 'pub_date']})]
	list_display = ('product_name', 'category', 'subcategory')
	inlines = [colorInline, memoryRomInline, memoryRamInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Pearl_Users)