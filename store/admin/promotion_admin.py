from django.contrib import admin
from store.models import *
from store.admin import product_admin,promotion_admin
class ProductOnPromotionalOffer(admin.StackedInline):
    model = PromotionalOffer.products.through                          #models.Promotion.products_on_promotion.through
    extra = 5
    raw_id_fields = ("product",)


@admin.register(PromotionalOffer)
class ProducList(admin.ModelAdmin):
    model = PromotionalOffer
    inlines = (ProductOnPromotionalOffer,)
    list_display = ("name", "is_active","is_scheduled", "offer_start", "offer_end")
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related(PromotionalOffer)
    

admin.site.register(Coupon)
admin.site.register(PromotionType)
