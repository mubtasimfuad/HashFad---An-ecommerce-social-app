from logging import exception
from venv import create
from django.db.models import Sum, Count
from store import pil, serializers
from django.db.models import Q

from store.models.product_models import Basket, BasketItem, Category, Order, Product, ProductVariation, Query, ReviewRating
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from store.models.user_models import Customer, Vendor
from store.permissions import IsAdminOrReadOnly, IsAuthor, IsProductVendor, IsVariationVendor, IsVendorOrReadOnly
from store.serializers import BasketItemAdditionSerializer, BasketItemSerializer, BasketItemUpdateSerializer, BasketToOrderSerializer, CategorySerializer, OrderSerializer, ProductSerializer, ProductVariationSerializer, QuerySerializer, ReviewRatingSerializer, BasketSerializer

 #@api_view()
# def product_list(request):
#     queryset = Product.objects.all().select_related('category').annotate(stock = Sum('variations__stock'))
#     serializer = ProductSerializer(queryset,many=True,  context={'request': request})
    
#     return Response(serializer.data)

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsProductVendor,IsVendorOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category').prefetch_related('variations').annotate(stock = 
        Sum('variations__stock'), total_variation = Count('variations'))
        
        category_id = self.request.query_params.get('category__id')

        if category_id is not None:
            queryset =  queryset.filter(category__id=category_id)

        return queryset

    def get_serializer_context(self):
        context = { 'request': self.request}
        return context

    def update(self, request, *args, **kwargs):
        
        return super().update(request, *args, **kwargs)
    

class VariationViewSet(ModelViewSet):
    serializer_class=ProductVariationSerializer
    permission_classes = [IsVariationVendor, IsVendorOrReadOnly]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request 
        return context

    def get_queryset(self):
    
        queryset =  ProductVariation.objects.all().select_related('product')
        product_id=  self.request.GET.get('product__id', None)
        if product_id:
            queryset = queryset.filter(product=product_id)

        return queryset
    
class CategoryViewSet(ModelViewSet):
    serializer_class=CategorySerializer
    queryset =  Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class ReviewRatingViewSet(ModelViewSet):
    serializer_class = ReviewRatingSerializer
    permission_classes=[IsAuthenticatedOrReadOnly, IsAuthor]
    def get_serializer_context(self):
        context = { "product_pk": self.kwargs['product_pk'], 'request': self.request}
        return context

    def get_queryset(self):
        product_id=  self.kwargs['product_pk']
        queryset = ReviewRating.objects.filter(product=product_id)
        return queryset
    
   
class QueryViewSet(ModelViewSet):
    serializer_class = QuerySerializer
    permission_classes=[IsAuthenticatedOrReadOnly, IsAuthor]

    def get_serializer_context(self):
        context = { "product_pk": self.kwargs['product_pk'], 'request': self.request}
        return context

    def get_queryset(self):
        product_id=  self.kwargs['product_pk']
        queryset = Query.objects.filter(Q(query=None) & Q(product=product_id))
        return queryset


class BasketViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, GenericViewSet):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all().prefetch_related('items__product__product')
    
    
class BasketItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_classes = {
        'POST': BasketItemAdditionSerializer,
        'PATCH': BasketItemUpdateSerializer,
        
    }

    default_serializer_class = BasketItemSerializer
    
    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.default_serializer_class)

    def get_queryset(self):
        queryset= BasketItem.objects .filter(
            basket_id=self.kwargs['basket_pk']).select_related('product__product')
        return queryset

    def get_serializer_context(self):
         return {'basket_pk':self.kwargs["basket_pk"]}

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes=[IsAuthenticated]

    serializer_classes = {
        'POST': BasketToOrderSerializer,
        
    }
    def create(self, request, *args, **kwargs):
        serializer = BasketToOrderSerializer(data=request.data, context= {'user_id': self.request.user.id, "request":self.request })
        serializer.is_valid(raise_exception=True)
        order_obj = serializer.save()
        if len(order_obj)<2:
         serializer = OrderSerializer(order_obj, many=True,context={"request":self.request } )
         return Response({"returned_data": serializer.data})
        else:
            serializer = OrderSerializer(order_obj[0],  many=True,context={"request":self.request })
            return Response({"returned_data": serializer.data, "stock_out_product":order_obj[1]})



    def get_serializer_context(self):
        return {"request":self.request}    
    def get_queryset(self):
        user=  self.request.user
        if user.is_staff:
            return Order.objects.all()

        if user.user_type == "customer":
            customer = Customer.objects.get(user_id=user.id)
            return Order.objects.filter(customer_id=customer.id)
        if user.user_type == "vendor":
            vendor = Vendor.objects.get(user_id=user.id)
            return Order.objects.filter(product__product__vendor__id=vendor.id)
   
    default_serializer_class = OrderSerializer
   

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.default_serializer_class)






    

