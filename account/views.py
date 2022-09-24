from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from account.models import Account
from account.serializers import EmailVerificationSerializer, RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings



# Create your views here.



class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = Account.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        absurl = 'http://'+current_site+relative_link+"?token="+str(token)

        email_body = ' Use the link below to verify your email \n'+absurl
        data = {'email_body': email_body, 'to_email': user.email,'name':user.first_name,
                'email_subject': 'Verify your email for HashFad'}
        
        Util.send_email(data)
       
        return Response(user_data, status=status.HTTP_201_CREATED)
class VerifyEmail(views.APIView):
      serializer_class = EmailVerificationSerializer
      def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = Account.objects.get(id=payload["user_id"])
            if not user.is_active:
                user.is_active = True
                user.save()
            else:
                return Response({'email': "Already Activated"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'email': "Succesfully Activated"}, status=status.HTTP_202_ACCEPTED)
        except jwt.ExpiredSignatureError as ex:
            return Response({'error': "Expired Signature"}, status=status.HTTP_202_ACCEPTED)

        except jwt.exceptions.DecodeError as ex:
            return Response({'error': "Invalid Token "}, status=status.HTTP_202_ACCEPTED)
