from email.policy import default
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField 
from django.conf import settings
from datetime import date
from django.template.defaultfilters import slugify
from store.models.product_models import Order

_current_year = str(date.today().year)[-2:]

# Create your models here.
class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    phone1 = PhoneNumberField(region='BD')
    phone2 = PhoneNumberField(region='BD',blank=True,null=True)
    class Meta:
        abstract = True

class DeliveryAgent(Address):
    nid = models.CharField(max_length=25)
    username = models.CharField(unique=True,blank=True,max_length=500)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.username = 'da'+_current_year+str(self.user.id)+"-"+slugify(self.user.first_name)+slugify(self.user.last_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class DeliveryTask(models.Model):
    agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL)
    delivery_time = models.DateTimeField()
    attempt = models.PositiveSmallIntegerField(default=0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    isReturned = models.BooleanField(default=False)
    remarks = models.TextField()

