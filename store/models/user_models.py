from django.db import models
from django.conf import settings
from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField 
from django.template.defaultfilters import slugify
from datetime import date

_current_year = str(date.today().year)[-2:]



class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    phone1 = PhoneNumberField(region='BD')
    phone2 = PhoneNumberField(region='BD',blank=True,null=True)
    class Meta:
        abstract = True


class Vendor(Address):
    username = models.CharField(unique=True,blank=True,max_length=500)
    store_name= models.CharField(max_length=300)
    birth_date = models.DateField(null=True, blank=True)
    nid = models.CharField(max_length=25)
    licence_id = models.CharField(max_length=25, blank=True,null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

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
        if not self.id:
            self.username = 'c'+_current_year+str(self.user.id)+"-"+slugify(self.user.first_name)+slugify(self.user.last_name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


