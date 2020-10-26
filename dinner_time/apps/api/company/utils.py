from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response

from apps.api.users.models import User
from apps.api.users.utils import *
from apps.utils.func_for_send_message import *


def create_user_or_company(company_name, serializer, parent=None, is_company=False):
    serializer.validated_data.update(generate_random_password_username())

    if User.objects.filter(phone=serializer.validated_data.get('phone')).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Phone number already in use.')

    user = create_user_account(parent=parent, **serializer.validated_data)
    upid = create_ref_link_for_update_auth_data(obj=user)

    send_message(company_name, upid, serializer.data, is_company)

    return Response(status=status.HTTP_201_CREATED)


def send_message(company_name, upid, data, is_company, is_recovery_password=False, login=None):
    if is_company and not is_recovery_password:
        url = settings.URL_FOR_CHANGE_AUTH_DATA_COMPANY + upid
        header, body = send_message_for_change_auth_data_company(company_name=company_name)
        text_password = "Установить пароль"

    elif is_recovery_password:
        change_url = settings.URL_FOR_RECOVERY_PASSWORD_COMPANY if is_company else settings.URL_FOR_RECOVERY_PASSWORD_USER
        url = change_url + upid
        header, body = send_message_for_recovery_password(login=login)
        text_password = "Изменить пароль"

    else:
        url = settings.URL_FOR_CHANGE_AUTH_DATA_USER + upid
        header, body = send_message_for_change_auth_data_client(company_name=company_name)
        text_password = "Установить пароль"

    message_data = {"welcome_message": body,
                    "registration_link": url,
                    "text_password": text_password}

    html_content = render_to_string('registration_message.html', message_data)
    text_content = strip_tags(html_content)
    msg_html = render_to_string('registration_message.html', message_data)

    send_mail(subject=header, message=text_content, from_email=settings.EMAIL_ADDRESS,
              recipient_list=[data.get('email')], html_message=msg_html)
