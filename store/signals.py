from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models.user_models import Customer, DeliveryAgent, Vendor
from django.conf import settings



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created,**kwargs):
    if created:
        if instance.user_type =='vendor':
            Vendor.objects.create(user=instance)
        if instance.user_type == 'customer':
            Customer.objects.create(user=instance)
        if instance.user_type == 'agent':
            DeliveryAgent.objects.create(user=instance)