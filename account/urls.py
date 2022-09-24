
from django.urls import path, include
from .views import RegisterView, VerifyEmail
urlpatterns = [
     path('register/', RegisterView.as_view(), name="register"),
     path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
     path('auth/', include('djoser.urls')),
     path('auth/', include('djoser.urls.jwt')),]