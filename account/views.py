from django.shortcuts import render,get_object_or_404
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from account.models import Account, ActivatorKey
from account.permissions import IsAnonymousUser
from account.serializers import EmailActivationSerializer, EmailVerificationSerializer, SignInSerializer, SignUpSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
import datetime, random, hashlib
from rest_framework.views import APIView
from mailjet_rest import Client
import os
from datetime import datetime,timedelta
# Create your views here.



class RegisterView(generics.GenericAPIView):

    serializer_class = SignUpSerializer
    permission_classes = [IsAnonymousUser]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = Account.objects.get(email=user_data["email"])
        salt = '%0*d%0*d' % (8, random.randint(0, 99999999), 8, random.randint(0, 99999999))
        activation_key = hashlib.md5((user.email+salt).encode("utf-8")).hexdigest()[:10]
        invalid_at=datetime.now() +timedelta(days=7) 
        ActivatorKey.objects.create(user=user,activation_key=activation_key,invalid_at=invalid_at)

        # token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-activate')
        mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')


        absurl = 'http://'+current_site+relative_link+"?activation_key="+str(activation_key)

        email_body = ' Use the link below to verify your email \n'+absurl
        body_html = f'''<html>
         <body>
        <h1>Hi,{user.first_name}</h1>
        {email_body}
        <footer>  <img src="https://i.ibb.co/5j3rTYp/logo.png" /></footer>
       </body>
      </html>'''
        data = {
        'Messages': [
            {
            "From": {
                "Email": "hashfad.info@gmail.com",
                "Name": "Hashfad"
            },
            "To": [
                {
                "Email":  user.email,
                "Name": user.first_name
                }
            ],
            "Subject": "Activate your hashfad account",
            "TextPart": "Thanks for choosing us",
            "HTMLPart": body_html,
            "CustomID": f"Activation{user.id}"
            }
        ]
        }
        result = mailjet.send.create(data=data)
        print (result.status_code)
        print (result.json())
        
       
        return Response(user_data, status=status.HTTP_201_CREATED)

# class VerifyEmail(views.APIView):
#       serializer_class = EmailVerificationSerializer
#       def get(self, request):
#         token = request.GET.get('token')

#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             user = Account.objects.get(id=payload["user_id"])
#             if not user.is_active:
#                 user.is_active = True
#                 user.save()
#             else:
#                 return Response({'email': "Already Activated"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             return Response({'email': "Succesfully Activated"}, status=status.HTTP_202_ACCEPTED)
#         except jwt.ExpiredSignatureError as ex:
#             return Response({'error': "Expired Signature"}, status=status.HTTP_202_ACCEPTED)

#         except jwt.exceptions.DecodeError as ex:
#             return Response({'error': "Invalid Token "}, status=status.HTTP_202_ACCEPTED)



class ActivateEmail(views.APIView):
      serializer_class = EmailActivationSerializer
      def get(self, request):
        activation_key = request.GET.get('activation_key')

        try:
            activator=get_object_or_404(ActivatorKey,activation_key=activation_key)
            print(activation_key,activator)
            if not activator.is_raised:
                user = Account.objects.get(id=activator.user.id)
                activator.is_raised=True
                activator.save()
                if not user.is_active:
                    user.is_active = True
                    user.save()
                else:
                    return Response({'key': "Used key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                    return Response({'key': "Expired Key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
          
            return Response({'email': "Succesfully Activated"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response( status=status.HTTP_406_NOT_ACCEPTABLE)




class SignInAPIView(generics.GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes=[IsAnonymousUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAPIView(APIView):
     def post(self, request, *args, **kwargs):
    
        api_key = '07ae3c77e4efbdfe71fe1e3343d9dfd6'
        api_secret = '1cb2736d6df186f2e9252f7bb7adda1b'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "hashfad.info@gmail.com",
                "Name": "Hashfad"
            },
            "To": [
                {
                "Email": "mubtasimfuadayon@gmail.com",
                "Name": "Mubtasim"
                }
            ],
            "Subject": "Greetings from Mailjet.",
            "TextPart": "My first Mailjet email",
            "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = mailjet.send.create(data=data)
        print (result.status_code)
        print (result.json())
        return Response({'error': "Invalid Token "}, status=status.HTTP_202_ACCEPTED)