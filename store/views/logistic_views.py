from rest_framework.viewsets import GenericViewSet, ModelViewSet
from store.paginations import ListPagination
from store.permissions import *
from rest_framework.permissions import IsAdminUser
from store.models.logistic_models import DeliveryTask
from store.serializers import DeliveryTaskSerializer, DeliveryTaskUpdateSerializer


class DeliveryTaskViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete','head','options']
    serializer_class=DeliveryTaskSerializer
    permission_classes = [IsAgent]
    pagination_class=ListPagination


    
    serializer_classes = {
        'POST': DeliveryTaskSerializer,
        'PATCH': DeliveryTaskUpdateSerializer,
        
    }

    default_serializer_class = DeliveryTaskSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return DeliveryTask.objects.all()
        else:
            return DeliveryTask.objects.filter(agent__user__id=self.request.user.id)
    

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.default_serializer_class)