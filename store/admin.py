from django.contrib import admin

from store.models.product_models import Basket, BasketItem, Category, Order, Product, ProductVariation, Query, ReviewRating
from store.models.user_models import Vendor, Customer
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariation)
admin.site.register(Category)
admin.site.register(ReviewRating)
admin.site.register(Query)
admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)







