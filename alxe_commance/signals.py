from .task import AccountCreation
from django.dispatch import receiver
from .models import User , Cart
from django.db.models.signals import post_save
from django.conf import settings



@receiver(post_save , sender = User)
def ConfirmedAccount(sender ,instance , created , **kwargs):
    
    if created:
        if instance.role == "BUYER":
            Cart.objects.create(buyer = instance)
        AccountCreation.delay(settings.DEFAULT_FROM_EMAIL , instance.username , instance.email)
