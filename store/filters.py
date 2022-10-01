from django_filters.rest_framework import FilterSet
from store.models.product_models import Product


class CustomProductFilter(FilterSet):
    class Meta:
        model=Product
        fields ={
            'category_id':['exact'],
            'price':['gt','lt'],
            'vendor':['exact']
        }