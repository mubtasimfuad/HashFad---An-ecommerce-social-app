
from decimal import Decimal
from itertools import product
from . import pil
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from store.models.product_models import Basket, BasketItem, Order,  Product, ProductVariation, Category, Query, ReviewRating
from store.models.user_models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'

class ProductVariationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductVariation
        fields = '__all__'
        none_to_str_fields = ('color', )
    def get_fields(self):
        fields = super().get_fields()
        fields['product'].queryset = Product.objects.filter(vendor__user__id=self.context["request"].user.id)
        return fields

    def validate(self, attrs):
        if attrs['color'] == "":
            attrs['color']= pil._get_image_field_color(attrs)
        return super().validate(attrs)

    # def create(self, validated_data):
    #     if validated_data['color'] == "":
    #         validated_data['color']= pil._get_image_field_color(validated_data)
    #         return super().create(validated_data)
    #     return super().create(validated_data)
    # def update(self, instance, validated_data):
    #     # if validated_data['color'] is None or "":
    #     validated_data['color'] = pil._get_image_field_color(instance.image)
    #     return super().update(instance, validated_data)
    
    
       

class ProductSerializer(serializers.ModelSerializer):
    variation = ProductVariationSerializer(source='variations',
                                  many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id','vendor_id','title', 'description', 'price', 'featured_image', 'is_available','category','stock','total_variation','slug','variation']
    
    stock = serializers.IntegerField(read_only=True)
    total_variation = serializers.IntegerField(read_only=True)
    read_only_fields = ["vendor_id"]

    def validate(self, attrs):


        attrs['vendor_id'] = int(self.context["request"].user.vendor_set.id)
        return attrs

class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        
        model= ReviewRating
        fields = ["product_id","user_id",'subject', 'review', 'rating']
        read_only_fields = ["product_id","user_id",]

    def validate(self, attrs):
        attrs["product_id"] = int(self.context["product_pk"])
        attrs["user_id"] = int(self.context["request"].user.id)

        return attrs
   
        
    # def validated_data(self):
    #     validated_data = super().validated_data
    #     validated_data["user"] = self.request.user.id 
    #     validated_data["product"] = self.context["product_pk"]
    #     return validated_data

class QuerySerializer(serializers.ModelSerializer):
  
    sub_query = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_query")

    class Meta:
        model= Query
        fields = ['id',"query",'product_id','user_id', 'body', "sub_query", ]
        read_only_fields = ["product_id","user_id",]
    
        
   
    def validate(self, attrs):
        attrs["product_id"] = int(self.context["product_pk"])
        attrs["user_id"] = int(self.context["request"].user.id)

        return attrs
    def get_child_query(self, obj):
        """ self referral field """
        serializer = QuerySerializer(
            instance=obj.query_reply.all(),
            many=True
        )
        return serializer.data
   

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

class ProductVariationCartSerializer(serializers.ModelSerializer):
     product = serializers.StringRelatedField()
     unit_price_with_tax = serializers.SerializerMethodField(read_only=True)

     class Meta:
        model = ProductVariation
        fields = ['product','image','unit_price_with_tax','color','size']
        read_only_fields = ['unit_price_with_tax']

     def get_unit_price_with_tax(self,object:ProductVariation):
        return object.price_after_add



class BasketItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    product = ProductVariationCartSerializer(read_only=True)

    def get_total_price(self, object):
        return round(object.quantity * Decimal(object.product.price_after_add),3)

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'total_price']
    

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(read_only=True, many=True)
    grand_total = serializers.SerializerMethodField(read_only=True)
    
    def get_grand_total(self,object:Basket):
        return sum([round((item.quantity * item.product.price_after_add),3) for item in object.items.all()])
    class Meta:
        model= Basket
        fields = ['id','items', 'grand_total']
        read_only_fields = ['id']


class BasketItemAdditionSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = BasketItem
        fields = ['id', 'product_id','quantity']
    def save(self, **kwargs):
        basket_id = self.context['basket_pk']
        product_id = self.validated_data['product_id']
        if not ProductVariation.objects.filter(product_id=product_id).exists():
            raise serializers.ValidationError({"product_id":"No Such Product Found"})
        

        quantity = self.validated_data['quantity']
        try:
            basket_item =BasketItem.objects.get(basket_id=basket_id, product_id=product_id)
            basket_item.quantity+=quantity
            basket_item.save()
        except:
            basket_item = BasketItem.objects.create(basket_id=basket_id, product_id=product_id, quantity=quantity)
        self.instance = basket_item
        return self.instance
            
class BasketItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['quantity']

class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    product = ProductVariationCartSerializer()


    class Meta:
        model = Order
        fields =['id','customer_id','product','quantity','total_price','placed_at',
        'delivery_status','payment_status','payment_method',
        ]
        


class BasketToOrderSerializer(serializers.Serializer):
    basket_id = serializers.UUIDField()

    
    def save(self, **kwargs):
        basket_id = self.validated_data['basket_id']
        basket = BasketItem.objects.filter(basket_id=basket_id)
        user_id = self.context['user_id']
        customer = Customer.objects.get(user_id=user_id)
        basket_object_list = []
        stocked_out_products = []
        
        
        for item in basket:
            if item.product.stock==0:
                stocked_out_products.append(item.product.id)
                continue
            print(item.product.product.title , item.product.price_after_add)
            order_object=Order(
                customer_id=customer.id,
                product = item.product,
                total_price= item.product.price_after_add,
                quantity = item.quantity
                    )
            basket_object_list.append(order_object)
        data = [Order.objects.bulk_create(basket_object_list, ignore_conflicts=True), stocked_out_products]
        return data
        #     if len(stocked_out_products)>0:
        #             return Response({"ok":basket_object_list,"stock_out":stocked_out_products},status=status.HTTP_201_CREATED)
        #     return Response({"ok":basket_object_list},status=status.HTTP_201_CREATED)
        # except Exception as ex:
        #         return Response({"error":ex},status=status.HTTP_400_BAD_REQUEST)
            
    



