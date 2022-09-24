
from django.urls import path, include
from .views import RegisterView, SignInAPIView, VerifyEmail
urlpatterns = [
     path('register/', RegisterView.as_view(), name="register"),
     path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
     path('signin/', SignInAPIView.as_view(), name="signin"),

     ]