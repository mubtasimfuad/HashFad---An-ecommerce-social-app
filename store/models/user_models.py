from logging import raiseExceptions
from django.db import models
from django.conf import settings
from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField 
from django.template.defaultfilters import slugify
from datetime import date

_current_year = str(date.today().year)[-2:]



class Address(models.Model):
    address = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    district = models.CharField(max_length=255,null=True)
    phone1 = PhoneNumberField(region='BD',null=True)
    phone2 = PhoneNumberField(region='BD',blank=True,null=True)
    class Meta:
        abstract = True


class Vendor(Address):
    username = models.CharField(unique=True,blank=True,max_length=500)
    store_name= models.CharField(max_length=300,null=True)
    birth_date = models.DateField(null=True, blank=True)
    nid = models.CharField(max_length=25,null=True)
    licence_id = models.CharField(max_length=25, blank=True,null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor_set")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        # if not self.id:
        self.username = 'v'+_current_year+str(self.user.id)+"-"+slugify(self.store_name)
        return super().save(*args, **kwargs)

   
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class Customer(Address):
    username = models.CharField(unique=True,blank=True,max_length=500)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        # isVendor = Vendor.objects.get(user=self.user.id)
        # if isVendor:
        #     raise PermissionError("Can't create a customer profile with the same id of vendor")
        if not self.id:
            self.username = 'c'+_current_year+str(self.user.id)+"-"+slugify(self.user.first_name)+slugify(self.user.last_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class DeliveryAgent(Address):
    nid = models.CharField(max_length=25,null=True)
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