from django.db import models
from store.models.product_models import Order
from store.models.user_models import DeliveryAgent


class DeliveryTask(models.Model):
    agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL)
    delivery_time = models.DateTimeField()
    attempt = models.PositiveSmallIntegerField(default=0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    isReturned = models.BooleanField(default=False)
    remarks = models.TextField()

