from django.shortcuts import render,get_object_or_404
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from account.models import Account, ActivatorKey
from account.permissions import IsAnonymousUser
from account.serializers import EmailActivationSerializer, EmailVerificationSerializer, SignInSerializer, SignUpSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from store.models.product_models import Product, ProductVariation
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
from .utils import format_html
# Create your views here.
from django.db import transaction 


class RegisterView(generics.GenericAPIView):

    serializer_class = SignUpSerializer
    permission_classes = [IsAnonymousUser]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        with transaction.atomic():
            user = Account.objects.get(email=user_data["email"])
            salt = '%0*d%0*d' % (8, random.randint(0, 99999999), 8, random.randint(0, 99999999))
            activation_key = hashlib.md5((user.email+salt).encode("utf-8")).hexdigest()[:10]
            invalid_at=datetime.now() +timedelta(days=7) 

            ActivatorKey.objects.create(user=user,activation_key=activation_key,invalid_at=invalid_at)

            # token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relative_link = reverse('email_activate')
            mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')

            link_to_submit = 'http://'+current_site+relative_link
            absurl = 'http://'+current_site+relative_link+"?activation_key="+str(activation_key)

            email_body = ' Use the link below to verify your email \n'+absurl
            body_html = format_html(user.first_name,activation_key,absurl,link_to_submit)
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



class ActivateEmail(generics.GenericAPIView):
    http_method_names = ['get', 'post','head']
    serializer_class = EmailActivationSerializer
 
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        activation_key=user["activation_key"].lower()
        print(activation_key)
            
       
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
            return Response({'key': "Invalid Key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @swagger_auto_schema(
    manual_parameters=[openapi.Parameter('activation_key', openapi.IN_QUERY, description="activation link concated with the url through email", type=openapi.TYPE_STRING)]
    )
    def get(self, request):
        """
        param1 -- activation_key

        """ 
     
        activation_key = request.GET.get('activation_key')
        if not activation_key ==None or "":
                
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
                return Response({'key': "Invalid Key"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("Post the activation key")



class SignInAPIView(generics.GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes=[IsAnonymousUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAPIView(APIView):
     import random
     def post(self, request, *args, **kwargs):
        product_list=[]
        size=['32','34','36','38','40','42','44','46','default']
        
        for item in range(50):
           
            # print(item.product.product.title , item.product.price_after_add)
            product_obj=ProductVariation(
                product_id = random.randint(1, 50),
                stock=random.randint(1, 10),
                color = "#23663"+str(random.randint(item, 50)),
                size = size[random.randint(0,8)],
                added_price = 20+item,
                    )
            product_list.append(product_obj)
            
        # basket_object_list.append(order_object)
        ProductVariation.objects.bulk_create(product_list)
        
        return Response({'success': "Created"}, status=status.HTTP_202_ACCEPTED)