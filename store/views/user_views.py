from store.models.user_models import Customer, Vendor
from store.serializers import CustomerSerializer, VendorSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin


class VendorViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = VendorSerializer
    queryset= Vendor.objects.all()

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CustomerSerializer
    queryset= Customer.objects.all()

