import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Announcement, Respond
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@receiver(post_save, sender=Respond)
def send_email_respond_confirmed(sender, instance, **kwargs):

    if instance.confirmed:
        user = instance.user

        ### Отправление письма ###
        email_message = EmailMultiAlternatives(
            subject='Отклик принят',
            body='',
            from_email=os.getenv('MAIN_EMAIL'),
            to=[user.email]
        )

        html_content = render_to_string(
            'account/email/respond_confirmed.html',
            {
                'username': user.username,
                'link_respond': f'http://127.0.0.1:8000/announcements/responds/{instance.id}',
                'link_announce': f'http://127.0.0.1:8000/announcements/{instance.announcement.id}',
            }
        )

        email_message.attach_alternative(html_content, 'text/html')
        email_message.send()


@receiver(post_save, sender=Respond)
def send_email_respond_created(sender, instance, **kwargs):

    if kwargs['created']:
        user = instance.announcement.user

        ### Отправление письма ###
        email_message = EmailMultiAlternatives(
            subject='Новый отклик',
            body='',
            from_email=os.getenv('MAIN_EMAIL'),
            to=[user.email]
        )

        html_content = render_to_string(
            'account/email/respond_content.html',
            {
                'username': user.username,
                'link_respond': f'http://127.0.0.1:8000/announcements/responds/{instance.id}',
                'link_announce': f'http://127.0.0.1:8000/announcements/{instance.announcement.id}',
            }
        )

        email_message.attach_alternative(html_content, 'text/html')
        email_message.send()


@receiver(post_save, sender=Announcement)
def send_email_announce_created(sender, instance, **kwargs):

    if kwargs['created']:
        user = instance.user
        user_list = User.objects.all().values_list('username', 'email')

        for _user in user_list:
            _username, _mail = _user[0], _user[1]

            if _mail != user.email:

                ### Отправление письма ###
                email_message = EmailMultiAlternatives(
                    subject='Новое объявление',
                    body='',
                    from_email=os.getenv('MAIN_EMAIL'),
                    to=[_mail]
                )

                html_content = render_to_string(
                    'account/email/announce_content.html',
                    {
                        'username': _username,
                        'link_announce': f'http://127.0.0.1:8000/announcements/{instance.id}',
                    }
                )

                email_message.attach_alternative(html_content, 'text/html')
                email_message.send()
