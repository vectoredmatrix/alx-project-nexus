from celery import shared_task
from django.core.mail import send_mail

@shared_task
def AccountCreation(sender_email , username , reciever_email ):
    send_mail(subject=f"Welcome {username}!",
              message="Your Account with ALX Ecommence Trading has be successfully created",
              from_email=sender_email,
              recipient_list=[reciever_email],
              html_message="<h1> Welcome !</h1><p>Thanks for Signing Up With Us")
    