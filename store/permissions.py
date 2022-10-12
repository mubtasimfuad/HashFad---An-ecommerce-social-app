from itertools import product
from rest_framework import permissions
from account.models import Account
from store.models.product_models import Order

from store.models.user_models import Customer, Vendor


class IsVendorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == "create":
            return  request.user.is_authenticated and request.user.user_type == "vendor"
               
        # else:
        #     return True
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS):
            return True
        elif (request.user.is_authenticated and request.user.is_staff):
                return True

class IsVariationVendor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
         if view.action == "retrieve":
            return True
         if view.action in ['update', 'partial_update','destroy']:
            
            if request.user.id == obj.product.vendor.user.id:
                return True

class IsProductVendorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user= request.user
        if (user.is_authenticated and user.is_staff):
            return True
        if view.action == "retrieve":
            return True
        if view.action in ['update', 'partial_update','destroy']:
            if request.user.id == obj.vendor.user.id:
                return True
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
    
        if view.action == "retrieve" :
            return True
        if view.action in ['update', 'partial_update','destroy']:
            
            if request.user.id == obj.user.id:
                return True
class IsVerifiedPurchase(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS):
            return True
            
        if view.action =="create":
            if Order.objects.filter(delivery_status="delivered",\
                product__product__pk=view.kwargs['product_pk'],invoice__customer__user__id=request.user.id).exists():
                return True 
    
        
                
        
        
                
            
    

class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            if request.user.is_authenticated:
                return False
            else:
                 return True
        else:
            return True
           
           
class IsAuthorizedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            if obj.user.user_type == "vendor":
                return True
            
        if view.action in ['update', 'partial_update','destroy']:
            
            if request.user.id == obj.product.vendor.user.id:
                return True
       
           
class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.user_type=="agent":
            if view.action in ['list','retrieve','update', 'partial_update']:
                return True
            else:
                 return False
        elif user.is_staff:
            return True 
class IsAuthorizedCustomer(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.customer.user.id == request.user.id or request.user.is_staff

     
           
class IsCustomerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "customer" or request.user.is_staff

        