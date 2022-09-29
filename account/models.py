from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyAccountManger(BaseUserManager):
    def create_user(self, first_name,last_name,email, user_type, password=None ):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must provide a first_name")
        if not last_name:
            raise ValueError("User must provide a last_name")
        if not user_type:
            raise ValueError("User must provide a user type")
        if not password:
            raise ValueError("User must provide a password")
        
        
        

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            user_type = user_type,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user 

    def create_superuser(self,  first_name,last_name, email, password,user_type):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            first_name = first_name,
            last_name = last_name,
            user_type=user_type,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using = self._db)

        return user

# GENDER_CHOICES = [
# ('male', 'Male'),
# ('female', 'Female'),
# ('other', 'Other')
# ]

USER_CHOICES = [
('staff','Staff'),
('vendor', 'Vendor'),
('customer', 'Customer'),
]


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100)
    user_type = models.CharField(max_length=25,choices=USER_CHOICES)
    # gender = models.CharField(choices=GENDER_CHOICES,max_length=8,  default='other')


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','user_type']
    objects = MyAccountManger()

    def __str__(self):
        return self.email+ " : "+str(self.pk)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        tokens={ 'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)}
        
        return tokens