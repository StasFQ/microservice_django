import datetime
import requests
from celery import shared_task
from django.core.mail import send_mail as django_send_mail
from celery import app

from .models import Order


@shared_task()
def send_order_to_store(order_id: int):
    order = Order.objects.get(id=order_id)
    #order_items = order.orderitem_set.all()

    body = {
        "user_email": order.user.email,
        "status": order.status,
        "delivery_adress": order.adress,
        "order_id_in_shop": order.id,
    }

    requests.post('http://storage:8001/api/create/', json=body)


@shared_task()
def send_order_item_to_store(order_id: int):
    order = Order.objects.get(id=order_id)
    order_items = order.orderitem_set.all()
    body = {
    'order_items': [
             {
                 'book_store_id': item.book.id_in_store,
                 'quantity': item.quantity
             } for item in order_items
         ]
    }
    requests.post('http://store:8001/api/create_item', json=body)