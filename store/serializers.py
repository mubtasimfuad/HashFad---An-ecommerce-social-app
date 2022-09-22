
from . import pil
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

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
      
    def validate(self, attrs):
        if attrs['color'] is None or "":
            attrs['color']= pil._get_image_field_color(attrs)
        return super().validate(attrs)
        
    
    
       

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','vendor','title', 'description', 'price', 'featured_image', 'is_available','category','stock','total_variation',]
    
    stock = serializers.IntegerField(read_only=True)
    total_variation = serializers.IntegerField(read_only=True)

class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= ReviewRating
        fields = ['user','subject', 'review', 'rating']

    def validate(self, attrs):
        if "product" not in attrs:
            attrs["product_id"] = int(self.context["product_pk"])

            return attrs
   
        
    # def validated_data(self):
    #     validated_data = super().validated_data
    #     validated_data["user"] = self.request.user.id 
    #     validated_data["product"] = self.context["product_pk"]
    #     return validated_data

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model= Query
        fields = ['product','user', 'body']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address','city','district','phone1','phone2']

class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields= ['id', 'user', 'store_name', 'birth_date', 'nid', 'licence_id','address', 'city','district','phone1']
        read_only_fields  = ('user',)
class VendorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields= ['id', 'user_id','username', 'store_name', 'birth_date', 'nid', 'licence_id','address', 'city','district','phone1','phone2']
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields= ['id', 'user_id','username', 'birth_date', 'address', 'city','district','phone1','phone2']
        read_only_fields = ('user_id',)
    # def create(self, validated_data):
    #     user_id = validated_data["user"]
    #     isVendor = Vendor.objects.get(user=user_id)
    #     if isVendor:
    #         return Response({"Multiple User Profile": "Can't create a customer profile with the same id of vendor"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().create(validated_data)

   
    
   


   
    # def get_stock(self, object: Product):
    #     return object.get_stock
    