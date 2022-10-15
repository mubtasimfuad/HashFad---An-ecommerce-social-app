from rest_framework.viewsets import ModelViewSet
from store.serializers import *
from rest_framework.permissions import IsAdminUser



class PromotionalOfferViewSet(ModelViewSet):
    serializer_class = PromotionalOfferSerializer
    model = PromotionalOffer
    queryset = PromotionalOffer.objects.all()
    permission_classes=[IsAdminUser]

class ProductPromotionalOfferViewSet(ModelViewSet):
    serializer_class = ProductPromotionalOfferSerializer
    model = ProductsOnPromotionalOffer
    queryset= ProductsOnPromotionalOffer.objects.all()
    permission_classes=[IsAdminUser]



    def get_serializer_context(self):
        context = { 'promotion_pk': self.kwargs.get('promotion_pk',None)}
        return context
    def get_queryset(self):
        queryset= ProductsOnPromotionalOffer.objects.filter(promotion_id=self.kwargs.get('promotion_pk',None))
        return queryset


