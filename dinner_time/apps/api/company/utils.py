from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
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


def send_message(company_name, upid, data, is_company):
    if is_company:
        url = settings.URL_FOR_CHANGE_AUTH_DATA_COMPANY + upid
        header, body = send_message_for_change_auth_data_company(company_name=company_name)
    else:
        url = settings.URL_FOR_CHANGE_AUTH_DATA_USER + upid
        header, body = send_message_for_change_auth_data_client(company_name=company_name)

    message_data = {"welcome_message": body,
                    "registration_link": url}

    email_html = get_template('registration_message.html')
    email_text = get_template('registration_message.txt')

    html_content = email_html.render(message_data)
    text_content = email_text.render(message_data)

    send_mail(
        header,
        text_content,
        settings.EMAIL_ADDRESS,
        [data.get('email')],
        html_message=html_content
    )


def check_oversupply_tariff(serializer_data, search_key, return_key):
    oversupply_tariff = 0
    for tariff in serializer_data:
        oversupply_tariff += tariff[search_key]

    return {
        return_key: oversupply_tariff,
        "data": serializer_data
    }
