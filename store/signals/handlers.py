from django.db.models.signals import post_save
from django.db.models import Count
from datetime import timedelta
from django.dispatch import receiver
from store.models.product_models import Invoice
from store.models.user_models import Customer, DeliveryAgent, Vendor
from store.models.logistic_models import DeliveryTask
from django.conf import settings
from . import invoice_created



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created,**kwargs):
    if created:
        if instance.user_type =='vendor':
            Vendor.objects.create(user=instance)
        if instance.user_type == 'customer':
            Customer.objects.create(user=instance)
        if instance.user_type == 'agent':
            DeliveryAgent.objects.create(user=instance)

@receiver(invoice_created)
def assign_order(sender,**kwargs):
    instance = kwargs["instance"]
    district = instance.customer.district
    city = instance.customer.city
    delivery_date = (instance.placed_at+timedelta(days=3)).date()
    print(instance)
    qs =DeliveryAgent.objects.filter(district=district,city=city)
    if qs.filter(tasks__delivery_time=delivery_date).count()<1:
            agent = qs.order_by('?').first()
    elif not qs.filter(tasks__delivery_time=delivery_date)\
            .annotate(tasks_count=Count('tasks')).filter(tasks_count__lte=10).count()<1:
            agent = qs.filter(tasks__delivery_time=delivery_date)\
            .annotate(tasks_count=Count('tasks')).filter(tasks_count__lte=10).order_by('?').first()
    else:
            agent = qs.filter(tasks__delivery_time=delivery_date)\
            .annotate(tasks_count=Count('tasks')).order_by('tasks_count').order_by('?').first()
    for order in instance.order_items.all():
        DeliveryTask.objects.create(agent=agent,delivery_time=delivery_date,order=order)
    