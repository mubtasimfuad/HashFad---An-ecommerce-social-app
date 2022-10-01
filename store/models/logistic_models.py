from django.db import models
from store.models.product_models import Order
from store.models.user_models import DeliveryAgent


class DeliveryTask(models.Model):
    agent = models.ForeignKey(DeliveryAgent, on_delete=models.CASCADE, related_name="tasks")
    delivery_time = models.DateField()
    attempt = models.PositiveSmallIntegerField(default=0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    isReturned = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True)
    remarks = models.TextField(null=True,blank=True)

