from django.contrib import admin
from .models import *
import nested_admin

class productImages(nested_admin.NestedStackedInline):
	model = ProductImages
	extra = 1

class imageInline(nested_admin.NestedStackedInline):
	model = ProductColorImages
	extra = 1

class colorInline(nested_admin.NestedStackedInline):
	model = ProductColor
	inlines = [imageInline]
	extra = 1

class memoryRomInline(nested_admin.NestedStackedInline):
	model = ProductMemoryRom
	extra = 0

class memoryRamInline(nested_admin.NestedStackedInline):
	model = ProductMemoryRam
	extra = 0

class ProductAdmin(nested_admin.NestedModelAdmin):
	fieldset = [(None, {'fields': ['product_name', 'category', 'subcategory', 'pub_date']})]
	list_display = ('product_name', 'category', 'subcategory')
	inlines = [productImages, colorInline, memoryRomInline, memoryRamInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Pearl_Users)



		


class myCartAdmin(admin.ModelAdmin):
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = myCart
admin.site.register(myCart, myCartAdmin)

admin.site.register(myCartItem)
admin.site.register(myVariance)

class myCatVariantAdmin(admin.StackedInline):
	model = myCategoryVariant
	extra = 0
class myCategoryAdmin(admin.ModelAdmin):
	inlines = [myCatVariantAdmin]
admin.site.register(myCategory, myCategoryAdmin)
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
	def get_formsets_with_inlines(self, request, obj=None):
		for inline in self.get_inline_instances(request, obj):
			if not isinstance(inline, myProductVariantAdmin) or obj is not None:
				yield inline.get_formset(request, obj), inline
	class Meta:
		model = myProduct

admin.site.register(myProduct, myProductAdmin)
