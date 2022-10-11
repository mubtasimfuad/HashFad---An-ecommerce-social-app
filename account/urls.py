
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ActivateEmail, RegisterView, SignInAPIView, TestAPIView #,VerifyEmail


urlpatterns = [
     # path('test/', TestAPIView.as_view(), name="test"),

     path('register/', RegisterView.as_view(), name="register"),
     # path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
     path('signin/', SignInAPIView.as_view(), name="signin"),

     path('email-activate/', ActivateEmail.as_view(), name="email_activate"),


     ]