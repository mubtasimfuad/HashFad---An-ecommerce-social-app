from django.db.models import Sum, Count
from store.models.product_models import Category, Product, ProductVariation, Query, ReviewRating
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from store.serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer, QuerySerializer, ReviewRatingSerializer

 #@api_view()
# def product_list(request):
#     queryset = Product.objects.all().select_related('category').annotate(stock = Sum('variations__stock'))
#     serializer = ProductSerializer(queryset,many=True,  context={'request': request})
    
#     return Response(serializer.data)

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category').prefetch_related('variations').annotate(stock = 
        Sum('variations__stock'), total_variation = Count('variations'))
        
        category_id = self.request.query_params.get('category__id')

        if category_id is not None:
            queryset =  queryset.filter(category__id=category_id)

        return queryset
    

class VariationViewSet(ModelViewSet):
    serializer_class=ProductVariationSerializer

    def get_queryset(self):
        queryset =  ProductVariation.objects.all()
        product_id=  self.request.GET.get('product__id', None)
        if product_id:
            queryset = queryset.filter(product=product_id)

        return queryset
    

    
    
class CategoryViewSet(ModelViewSet):
    serializer_class=CategorySerializer
    queryset =  Category.objects.all()


class ReviewRatingViewSet(ModelViewSet):
    serializer_class = ReviewRatingSerializer
    def get_serializer_context(self):
        context = { "product_pk": self.kwargs['product_pk'], 'request': self.request}
        return context

    def get_queryset(self):
        product_id=  self.kwargs['product_pk']
        queryset = ReviewRating.objects.filter(product=product_id)
        return queryset
    
   
class QueryViewSet(ModelViewSet):
    serializer_class = QuerySerializer

    def get_queryset(self):
        product_id=  self.kwargs['product_pk']
        queryset = Query.objects.filter(product=product_id)
        return queryset
    

   
    

