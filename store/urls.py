from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import product_views, user_views

router = routers.DefaultRouter()
router.register('products', product_views.ProductViewSet, basename='products')
router.register('variations', product_views.VariationViewSet, basename='product_variations')
router.register('category', product_views.CategoryViewSet)
router.register('vendors',user_views.VendorViewSet)
router.register('customers',user_views.CustomerViewSet)


product_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
product_router.register('reviews',product_views.ReviewRatingViewSet, basename="reviews")
product_router.register('queries',product_views.QueryViewSet, basename="queries")




urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),

    # path('store/',views.get_products_category, name="get_products_category"),
]