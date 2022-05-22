
from django.contrib import admin
from .models import *
import nested_admin

admin.site.register(Pearl_Users)

class CategoryVariantInline(admin.StackedInline):
	model = CategoryVariant
	extra = 0
class myCategoryAdmin(admin.ModelAdmin):
	inlines = [CategoryVariantInline]
admin.site.register(Category, myCategoryAdmin)

class ProductVariantValueInline(nested_admin.NestedStackedInline):
	model = ProductVariantValue
	extra = 0
class ProductVariantInline(nested_admin.NestedStackedInline):
	model = ProductVariant
	inlines = [ProductVariantValueInline]
	extra = 0
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'variant_type':
			try:
				product_id = request.resolver_match.kwargs.get('object_id')
				product = Product.objects.get(id = product_id)
				if product:
					kwargs["queryset"] = CategoryVariant.objects.filter(category = product.category)
			except:
				pass
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
class myProductColorImagesInline(nested_admin.NestedStackedInline):
	model = ProductColorImages
	extra = 0
class myProductColorInline(nested_admin.NestedStackedInline):
	model = ProductColor
	inlines = [myProductColorImagesInline]
	extra = 0
class myProductImageInline(nested_admin.NestedStackedInline):
	model = ProductImages
	extra = 0
class ProductAdmin(nested_admin.NestedModelAdmin):
	date_hierarchy = 'timestamp'
	search_fields = ['product_name']
	list_display = ('product_name', 'price', 'updated')
	readonly_fields = ['updated', 'timestamp']
	prepopulated_fields = {"slug":("product_name",)}
	inlines = [myProductColorInline, myProductImageInline, ProductVariantInline]
	def get_formsets_with_inlines(self, request, obj=None):
		for inline in self.get_inline_instances(request, obj):
			if not isinstance(inline, ProductVariantInline) or obj is not None:
				yield inline.get_formset(request, obj), inline
	class Meta:
		model = Product
admin.site.register(Product, ProductAdmin)

class myCartAdmin(admin.ModelAdmin):
	readonly_fields = ['updated', 'timestamp']
	class Meta:
		model = Cart
admin.site.register(Cart, myCartAdmin)

admin.site.register(CartItem)




