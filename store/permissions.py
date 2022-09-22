from rest_framework import permissions
from account.models import Account

from store.models.user_models import Customer, Vendor


class IsVendorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == "create":
            if request.user and request.user.user_type == "vendor":
                return True
        else:
            return True

class IsVariationVendor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
         if view.action == "retrieve":
            return True
         if view.action in ['update', 'partial_update','destroy']:
            
            if request.user.id == obj.product.vendor.user.id:
                return True

class IsProductVendor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
         if view.action == "retrieve":
            return True
         if view.action in ['update', 'partial_update','destroy']:
            
            if request.user.id == obj.vendor.user.id:
                return True
       
       
        