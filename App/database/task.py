from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_task(correos:list,evento):

    subject = 'Información de Un Nuevo Evento'
    html_message = render_to_string('templates/notificacion_evento.html', evento)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, correos, html_message=html_message,fail_silently=True)