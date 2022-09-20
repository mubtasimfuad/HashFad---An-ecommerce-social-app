
from . import pil
from rest_framework import serializers
from store.models.product_models import Product, ProductVariation, Category, Query, ReviewRating
from store.models.user_models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'

class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__'
    
    def create(self, validated_data):
        if validated_data['color'] is None or "":
            validated_data['color']= pil._get_image_field_color(validated_data)
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if validated_data['color'] is None or "":
            validated_data['color'] = pil._get_image_field_color(instance.image)
        return super().update(instance, validated_data)
       

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','vendor','title', 'description', 'price', 'featured_image', 'is_available','category','stock','total_variation',]
    
    stock = serializers.IntegerField(read_only=True)
    total_variation = serializers.IntegerField(read_only=True)

class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= ReviewRating
        fields = ['product','user', 'subject', 'review', 'rating']
class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model= Query
        fields = ['product','user', 'body']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address','city','district','phone1','phone2']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields= ['id', 'user','username', 'store_name', 'birth_date', 'nid', 'licence_id','address']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields= ['id', 'user','username', 'birth_date', 'address']


   
    
   


   
    # def get_stock(self, object: Product):
    #     return object.get_stock
    