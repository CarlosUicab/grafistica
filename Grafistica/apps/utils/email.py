# -*- coding: utf-8 -*-
import sys
import hashlib
from django.core.mail import EmailMultiAlternatives
from .extras import format_sys_errors


def send_email(subject, content, to, content_type="text/plain"):
    """
    Envía un email con el contenido que se le designe.
    :param subject: Título del email.
    :param content: contenido o body del mensaje.
    :param content_type: tipo de contenido Ej. "text/plain"
    :param to: lista de usuarios a los que llegará el email.
    :return: True o False para confirmar el envío.
    """
    try:
        msg = EmailMultiAlternatives(subject=subject, body=content, to=to)
        if content_type == "text/html":
            msg.attach_alternative(content, "text/html")
        msg.send()
    except:
        message = format_sys_errors(sys, with_traceback=True)
