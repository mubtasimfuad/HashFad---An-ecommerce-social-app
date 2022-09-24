from django.db import models
from django.db.models import Sum
from django.conf import settings
from store import pil
from store.models.user_models import Vendor, Customer
from django.core.validators import MinValueValidator
from uuid import uuid4
from decimal import Decimal

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("get_product_by_category", args=[self.slug])
# Create your models here.
class Product(models.Model):
    title    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=4000, blank=True)
    price           = models.DecimalField(max_digits=7, decimal_places=2)
    featured_image  = models.ImageField(upload_to='photos/products', default='no.jpg')
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    created_at    = models.DateTimeField(auto_now_add=True)
    modified_at   = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    

    
    class Meta:
        ordering = ('-modified_at',)

    def __str__(self) -> str:
        return self.title 
    # @property
    # def get_stock(self):
    #     stock = ProductVariation.objects.filter(product=self.id).prefetch_related('product').aggregate(Sum('stock'))['stock__sum']
    #     return stock



    # def get_absolute_url(self):
    #     return reverse("get_product_details", args=[self.category.slug,self.slug])
CHOICES=[
    ('32','32'),('34','34'),( '36', '36'),('38', '38'),('40','40'),
 ( '42', '42'),('44','44'),('46','46'), ('default','Default')]

class ProductVariation(models.Model):
    
    product = models.ForeignKey('Product', related_name='variations', on_delete= models.CASCADE)
    image   = models.ImageField(upload_to='photos/products', null =True)
    stock   = models.PositiveIntegerField()
    added_price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    color = models.CharField(max_length=50,null = True, blank=True, default=None)
    size = models.CharField(choices=CHOICES, null=True, max_length=20, default='default')
    class Meta:
        unique_together = ["product","color", "size"]
    
    def save(self,*args, **kwargs):
        if self.color is None or "":
            self.color = pil._get_image_field_color(self)
        
        return super().save(*args, **kwargs)
    @property
    def tax(self):
        return (self.product.price + self.added_price)* Decimal(0.2)
    @property
    def price_after_add(self):
        return self.product.price + self.added_price +self.tax


    def __str__(self):
        return self.product.title 


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Query(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="query")
    body = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    query = models.ForeignKey('self',on_delete=models.CASCADE, related_name='query_reply', default=None, null=True, blank=True)

    def __str__(self):
        return self.body[:30]

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def grand_total(self):
        sum([round((item.quantity * item.product.price_after_add),3) for item in self.items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]

class Order(models.Model):
    PENDING_STATUS = 'pending'
    SUCCESSFUL_STATUS = 'successful'
    FAILED_STATUS = 'failed'
    #############################
    PROCESSING_STATUS = 'processing'
    SHIPPED_STATUS = 'shipped'
    DELIVERED_STATUS = 'delivered'
    REUTRNED_STATUS = 'returned'


    PAYMENT_STATUS_CHOICES = [
        (PENDING_STATUS, 'Pending'),
        (SUCCESSFUL_STATUS, 'Successful'),
        (FAILED_STATUS, 'Failed'),
    ]
    
    DELIVERY_STATUS_CHOICES = [
        (PROCESSING_STATUS, 'Processing'),
        (SHIPPED_STATUS, 'Shipped'),
        (DELIVERED_STATUS, 'Delivered'),
        (REUTRNED_STATUS, 'Returned'),

    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(
        max_length=25, choices=DELIVERY_STATUS_CHOICES, default=PENDING_STATUS)
    payment_status = models.CharField(
        max_length=25, choices=PAYMENT_STATUS_CHOICES, default=PROCESSING_STATUS)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        ProductVariation, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()


    