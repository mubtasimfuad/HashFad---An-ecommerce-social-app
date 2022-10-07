from logging import exception
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.db.models import Q
from rest_framework.decorators import action
from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import CustomProductFilter
from store.models.product_models import Basket, BasketItem, Category, Invoice, Order, Product, ProductVariation, Query, ReviewRating
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from store.models.user_models import Customer, Vendor
from store.paginations import ListPagination
from store.permissions import IsAdminOrReadOnly, IsAnonymousUser, IsAuthor, IsAuthorizedCustomer, IsCustomerOrAdmin, IsProductVendorOrAdmin, IsVariationVendor, IsVendorOrReadOnly
from store.serializers import BasketItemAdditionSerializer, BasketItemSerializer, BasketItemUpdateSerializer, BasketToOrderSerializer, CategorySerializer, InvoiceSerializer, OrderSerializer, ProductSerializer, ProductVariationSerializer, QuerySerializer, ReviewRatingSerializer, BasketSerializer
import stripe
 #@api_view()
# def product_list(request):
#     queryset = Product.objects.all().select_related('category').annotate(stock = Sum('variations__stock'))
#     serializer = ProductSerializer(queryset,many=True,  context={'request': request})
    
#     return Response(serializer.data)
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsProductVendorOrAdmin,IsVendorOrReadOnly]
    pagination_class=ListPagination
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['category_id', 'vendor','price']
    filterset_class = CustomProductFilter
    search_fields = ['title','description','vendor__store_name','category__title']
    ordering_fields = ['price']

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category').prefetch_related('variations').annotate(stock = 
        Sum('variations__stock'), total_variation = Count('variations'))
        return queryset

    def get_serializer_context(self):
        context = { 'request': self.request}
        return context

    def update(self, request, *args, **kwargs):
        
        return super().update(request, *args, **kwargs)
    

class VariationViewSet(ModelViewSet):
    serializer_class=ProductVariationSerializer
    permission_classes = [IsVariationVendor, IsVendorOrReadOnly]
    pagination_class=ListPagination

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
    pagination_class=ListPagination
    

    def get_serializer_context(self):
        context = { "product_pk": self.kwargs.get('product_pk',None), 'request': self.request}
        return context

    def get_queryset(self):
        product_id=  self.kwargs.get('product_pk',None)
        queryset = ReviewRating.objects.filter(product=product_id)
        return queryset
    
   
class QueryViewSet(ModelViewSet):
    serializer_class = QuerySerializer
    permission_classes=[IsAuthenticatedOrReadOnly, IsAuthor]
    pagination_class=ListPagination


    def get_serializer_context(self):
        context = { "product_pk": self.kwargs.get('product_pk',None), 'request': self.request}
        return context

    def get_queryset(self):
        product_id=  self.kwargs.get('product_pk',None)
        queryset = Query.objects.filter(Q(query=None) & Q(product=product_id))
        return queryset


class BasketViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, GenericViewSet):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all().prefetch_related('items__product__product')
    # permission_classes=[IsCustomerOrAdmin]
   

    
class BasketItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_classes = {
        'POST': BasketItemAdditionSerializer,
        'PATCH': BasketItemUpdateSerializer,
        
    }

    default_serializer_class = BasketItemSerializer
    # permission_classes=[ IsCustomerOrAdmin]
    
    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.default_serializer_class)

    def get_queryset(self):
        queryset= BasketItem.objects .filter(
            basket_id=self.kwargs.get('basket_pk',None)).select_related('product__product')
        return queryset

    def get_serializer_context(self):
         return {'basket_pk':self.kwargs.get('basket_pk',None)}

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes=[IsAuthenticated,IsCustomerOrAdmin]
    pagination_class=ListPagination


    serializer_classes = {
        'POST': BasketToOrderSerializer,
        
    }
    default_serializer_class =InvoiceSerializer #OrderSerializer
   

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BasketToOrderSerializer
        return self.default_serializer_class

    def create(self, request, *args, **kwargs):
        serializer = BasketToOrderSerializer(data=request.data, context= {'user_id': self.request.user.id, "request":self.request })
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
       
        serializer = InvoiceSerializer(data[0])
        return Response({"returned_data": serializer.data, 'stocked_out':data[1]})


    def get_serializer_context(self):
        return {"request":self.request,'user_id': self.request.user.id}    
    def get_queryset(self):
        user=  self.request.user
        if user.is_staff:
            return Invoice.objects.all()
        else:
            try:
                customer = Customer.objects.get(user_id=user.id).first()
                return Invoice.objects.filter(customer_id=customer.id)
            except:
                 return None
        # if user.user_type == "vendor":
        #     vendor = Vendor.objects.get(user_id=user.id)
        #     return Invoice.objects.filter(product__product__vendor__id=vendor.id)
    # @action(detail=True,url_path='pay', methods=["POST"], permission_classes=[IsAuthenticated])

class PayStripe(APIView):
    def post(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=self.kwargs.get("order_pk",None))
        
        order_items = []

        for order_item in invoice.order_items.all():
            product:ProductVariation = order_item.product
            quantity = order_item.quantity

            data = {
                'price_data': {
                    'currency': 'bdt',
                    'unit_amount_decimal': round((product.price_after_add),3)*100,
                    'product_data': {
                        'name': product.product.title,
                        'description': product.product.description+" "+f"Color: {product.color}"+" "+f"Size: {product.size}"+" ",
                        'images':['https://static-01.daraz.com.bd/p/6b5147870171629254071485f4e65979.jpg'],
                        }
                },
                'quantity': quantity
            }

            order_items.append(data)

        # serializer = CustomerSerializer(customer)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=order_items,
                metadata={
                    "invoice_id": invoice.id
                },
                mode='payment',
                success_url='http://127.0.0.1:8000/backend/api/v1/store/orders/'+ '?success=true',
                cancel_url='http://127.0.0.1:8000/backend/api/v1/store/orders/' + '?canceled=true',
            )
            return Response({'sessionId': checkout_session['id'],"redirect_url": checkout_session.url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)



class StripeWebhookAPIView(APIView):
    """
    Stripe webhook API view to handle checkout session completed and other events.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret)
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            invoice_id = session['metadata']['invoice_id']

            print('Payment successfull')

            invoice = get_object_or_404(Invoice, id=invoice_id)
            invoice.payment_status = 'successful'
            invoice.save()
            # TODO - Decrease product quantity
            # send_payment_success_email_task.delay(customer_email)

        # Can handle other events here.

        return Response(status=status.HTTP_200_OK)





    

