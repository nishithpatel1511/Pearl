from pyexpat import model
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



		


class myCartAdmin(admin.ModelAdmin):
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = myCart
admin.site.register(myCart, myCartAdmin)

admin.site.register(myCartItem)
admin.site.register(myVariance)
admin.site.register(myCategory)
admin.site.register(myCategoryVariant)
# admin.site.register(myProductVariant)

class myProductVariantValueAdmin(nested_admin.NestedStackedInline):
	model = myProductVariantValue
	extra = 0

class myProductVariantAdmin(nested_admin.NestedStackedInline):
	model = myProductVariant
	inlines = [myProductVariantValueAdmin]
	extra = 0

class myProductAdmin(nested_admin.NestedModelAdmin):
	date_hierarchy = 'timestamp'
	search_fields = ['product_name']
	list_display = ('product_name', 'price', 'updated')
	readonly_fields = ['updated', 'timestamp']
	prepopulated_fields = {"slug":("product_name",)}
	inlines = [myProductVariantAdmin]
	class Meta:
		model = myProduct

admin.site.register(myProduct, myProductAdmin)
