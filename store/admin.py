from django.contrib import admin

from store.models.product_models import Category, Product, ProductVariation, Query, ReviewRating
from store.models.user_models import Vendor, Customer
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariation)
admin.site.register(Category)
admin.site.register(ReviewRating)
admin.site.register(Query)
admin.site.register(Vendor)
admin.site.register(Customer)





