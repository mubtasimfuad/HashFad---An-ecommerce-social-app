from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from store.views import logistic_views, promotion_views
from .views import product_views, user_views
app_name = 'store'
router = routers.DefaultRouter()
router.register('category', product_views.CategoryViewSet)
router.register('products', product_views.ProductViewSet, basename='products')
router.register('promotional-offers',  promotion_views.PromotionalOfferViewSet, basename='promotional_offers')
# router.register('product-on-offers',  promotion_views.ProductPromotionalOfferViewSet, basename='products_on_offer')

router.register('basket', product_views.BasketViewSet)
router.register('orders', product_views.OrderViewSet, basename="orders")
router.register('delivery-tasks', logistic_views.DeliveryTaskViewSet, basename="delivery_tasks")
router.register('vendors',user_views.VendorViewSet)
router.register('customers',user_views.CustomerViewSet)



product_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
product_router.register('reviews',product_views.ReviewRatingViewSet, basename="reviews")
product_router.register('queries',product_views.QueryViewSet, basename="queries")
product_router.register('variations',product_views.VariationViewSet, basename="product_variations")

basket_router = routers.NestedDefaultRouter(router, r'basket', lookup='basket')
basket_router.register('basket-items',product_views.BasketItemViewSet,basename="basket_products")

promotion_router=  routers.NestedDefaultRouter(router, r'promotional-offers', lookup='promotion')
promotion_router.register('products',promotion_views.ProductPromotionalOfferViewSet,basename="products_on_promotion")

urlpatterns = [

    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(basket_router.urls)),
    path('', include(promotion_router.urls)),
    
    path('orders/<int:invoice_pk>/pay',
         product_views.PayStripe.as_view(), 
         name='checkout_session'),
    path('orders/stripe/webhook', 
    product_views.StripeWebhookAPIView.as_view(), 
    name='stripe_webhook'),




    # path('store/',views.get_products_category, name="get_products_category"),
]