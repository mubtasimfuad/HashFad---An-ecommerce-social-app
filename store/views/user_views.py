from store.models.user_models import Customer, Vendor
from store.permissions import IsAdminOrReadOnly, IsAnonymousUser
from store.serializers import CustomerSerializer, VendorCreateSerializer, VendorBaseSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response



class VendorViewSet(ModelViewSet):
    queryset= Vendor.objects.all()
    permission_classes = [IsAnonymousUser]
    lookup_field="username"
    lookup_url_kwarg="username"
    serializer_classes = {
        'create': VendorCreateSerializer,
    }

    default_serializer_class = VendorBaseSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
    
    def create(self, request, *args, **kwargs):
        kwargs['user_id'] = request.user
        return super().create(request, *args, **kwargs)

    def perform_destroy(self, instance):
        #will add some logic to delete account after a period 
        return super().perform_destroy(instance)
    
   
    



class CustomerViewSet(CreateModelMixin,ListModelMixin,GenericViewSet):
    serializer_class = CustomerSerializer
    queryset= Customer.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    
    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        isVendor = Vendor.objects.filter(user=user_id)
        if isVendor:
            return Response({"Multiple User Profile": "Can't create a customer profile with the same id of vendor"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().create(request, *args, **kwargs)
        
    @action(detail=False,url_path='profile', methods=["GET","PUT","PATCH"], permission_classes=[IsAuthenticated])
    def get_user_profile(self,request):
        
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        if request.method == "PUT" or "PATCH":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
