from django.db import transaction
from datetime import datetime, timedelta
from math import ceil
from decimal import Decimal
from celery import shared_task
from store.models.product_models import Basket, BasketItem
from mailjet_rest import Client
from store.models.promotion_models import PromotionalOffer
from store.models.user_models import *
from django.conf import settings
from .utils import format_html

@shared_task()
def offer_promotions(discount_percent,object_id):
     with transaction.atomic():
        promotional_offers = PromotionalOffer.products.through.objects.filter(promotion_id=object_id)
        reduction = discount_percent / 100

        for offer in promotional_offers:
            if offer.price_override == False:
                price = offer.product.price
                new_price = ceil(price - (price * Decimal(reduction)))
                offer.promo_price = Decimal(new_price)
                offer.save()




@shared_task()
def delete_idle_cart(basket_id):
    with transaction.atomic():
        basket = Basket.objects.get(id = basket_id)
        if basket:
            current_date = datetime.now().date()
            if basket.created_at.date()< current_date:
                idol_duration = current_date-basket.created_at.date()
                if idol_duration==timedelta(days=15):
                    basket.delete() #deletes idle baskets after 15 days
                       

@shared_task
def send_emails_if_birthday():
        send_birthday_email()


                


@shared_task()
def manage_promotions():
    with transaction.atomic():
        promotional_offers = PromotionalOffer.objects.filter(is_scheduled=True)

        current_date = datetime.now().date()

        for offer in promotional_offers:
            if offer.is_scheduled:
                if offer.offer_end < current_date:
                    offer.is_active = False
                    offer.is_scheduled = False
                else:
                    if offer.offer_end <= current_date:
                        offer.is_active = True
                    else:
                        offer.is_active = False
            offer.save()




@shared_task
def send_birthday_email():
    customers = Customer.objects.filter(user__is_active=True, birth_date__isnull=False)
    now = datetime.today()
    for customer in customers:
        if customer.birth_date.day == now.day and customer.birth_date.month == now.month:
            mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
            html_data = {"name":customer.user.first_name+ " "+customer.user.last_name 
                }
            body_html =format_html(html_data)
            data = {
        'Messages': [
            {
            "From": {
                "Email": "hashfad.info@gmail.com",
                "Name": "Hashfad"
            },
            "To": [
                {
                "Email":  customer.user.email,
                "Name": customer.user.first_name
                }
            ],
            "Subject": "Birthday Wishes from HashFad Family",
            "TextPart": "Happy Birthday",
            "HTMLPart": body_html,
            "CustomID": f"HBD{customer.user.id}"
            }
        ]
        }
            result = mailjet.send.create(data=data)

            print (result.status_code)
            print (result.json())

        