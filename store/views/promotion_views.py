from rest_framework.viewsets import ModelViewSet
from store.serializers import *



class PromotionalOfferViewSet(ModelViewSet):
    serializer_class = PromotionalOfferSerializer
    model = PromotionalOffer
    queryset = PromotionalOffer.objects.all()

class ProductPromotionalOfferViewSet(ModelViewSet):
    serializer_class = ProductPromotionalOfferSerializer
    model = ProductsOnPromotionalOffer
    queryset= ProductsOnPromotionalOffer.objects.all()


    def get_serializer_context(self):
        context = { 'promotion_pk': self.kwargs.get('promotion_pk',None)}
        return context
    def get_queryset(self):
        queryset= ProductsOnPromotionalOffer.objects.filter(promotion_id=self.kwargs.get('promotion_pk',None))
        return queryset


