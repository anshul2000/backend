from twilio.rest import Client

from django.db.models.signals import post_save
from django.dispatch import receiver

from .form_data import get_phone_numbers
from .models import Message


@receiver(post_save, sender=Message)
def send_message(sender, instance, created, **kwargs):
    print('SENDING MESSAGES')
    content = instance.content
    district = instance.district
    if created:
        phone_numbers = get_phone_numbers(district)
        for phone_number in phone_numbers:
            try:
                client = Client('AC255cbc363184848e2bc6991b3912862e', '6b81f11412c6b38b3821241469e70db5')
                message = client.messages.create(from_='+13203078886', body=content, to=phone_number)
                print('Message status', message.status)
            except:
                print('Error sending message to', phone_number)
