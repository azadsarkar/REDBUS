from django.contrib.auth.signals import user_logged_in, user_logged_out,user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in, sender = User)
def login_success(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    request.session['ip'] = ip
    objects = user.first_name
    address = user.email
    masseges = f'Hello {objects} your account are login in this IP address{ip}'
    send_mail(objects, masseges, settings.EMAIL_HOST_USER, [address])