from django.db import models
from store.models.product_models import Order
from store.models.user_models import DeliveryAgent
from datetime import datetime


class DeliveryTask(models.Model):
    agent = models.ForeignKey(DeliveryAgent, on_delete=models.CASCADE, related_name="tasks")
    delivery_time = models.DateField()
    attempt = models.PositiveSmallIntegerField(default=0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    isReturned = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True,blank=True,editable=False)
    remarks = models.TextField(null=True,blank=True)

    def save(self,*args, **kwargs) -> None:
        if self.isDelivered:
            self.delivered_at = datetime.now()
            self.isReturned =False
        return super().save(*args, **kwargs)
 
    def __str__(self) -> str:
        return self.agent.username + " "+ str(self.order) + " ("+str(self.delivery_time)+" )"

