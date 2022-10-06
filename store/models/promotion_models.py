from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from store.models.product_models import Product

class PromotionType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        
        return self.name


class Coupon(models.Model):
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=20)

class PromotionalOffer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    offer_start = models.DateField()
    offer_end = models.DateField()
    promo_reduction = models.FloatField(default=0)
    is_scheduled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
   
    products = models.ManyToManyField(Product, 
    related_name="promotional_offer_products",       
    through="ProductsOnPromotionalOffer",
)
    promo_type = models.ForeignKey(
        PromotionType,
        related_name="promotional_offer_promo_type",
        on_delete=models.PROTECT,
    )
    coupon = models.ForeignKey(Coupon,related_name="promotional_offer_coupon",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
  

    def clean(self):
        if self.offer_start and self.offer_end:
            if self.offer_start > self.offer_end:
                raise ValidationError(("End date is prior than the start date"))

    def __str__(self):
        return self.name




class ProductsOnPromotionalOffer(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="product_on_promotional_offer_product",
        on_delete=models.PROTECT,
    )
    promotion = models.ForeignKey(
        PromotionalOffer,
        related_name="product_on_promotional_offer_promotion",
        on_delete=models.CASCADE,
    )
    promo_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )
    price_override = models.BooleanField(
        default=False,
    )

    class Meta:
        unique_together = (("product", "promotion"),)
