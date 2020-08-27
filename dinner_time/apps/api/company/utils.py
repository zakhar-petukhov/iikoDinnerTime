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


# TODO: соединить две функции "check_oversupply_tariff" и "create_companies_structure" вместе, чтобы упростить сложность
def check_oversupply_tariff(serializer_data, search_key, return_key, for_admin=False):
    # Function to calculate the monthly exceedance of the limit for the employees of the company, as well
    # as exceedance of the limit of the entire order of the company for the administrator

    oversupply_tariff = 0
    for tariff in serializer_data:
        oversupply_tariff += tariff[search_key]

    dinner_data = {
        return_key: oversupply_tariff,
        "data": serializer_data
    }

    if for_admin:
        return create_companies_structure(dinner_data)

    return dinner_data


def create_companies_structure(dinner_data):
    # We create our own structures, to be issued to the front.
    # Sort people by working groups and tie the lunches to them.

    company_structure = dict()

    dinners_data = dinner_data['data']
    full_oversupply_tariff = dinner_data.get('full_oversupply_tariff')

    for data in dinners_data:
        company_structure.update({
            'company': data['company']
        })

        for information in data['dinners']:
            department_name = information['user']['group']['name']

            if not company_structure.get(department_name):
                company_structure[department_name] = list()

            company_structure.get(department_name).append({
                "person": {
                    "id": information['user']['id'],
                    "first_name": information['user']['first_name'],
                    "last_name": information['user']['last_name'],
                    "middle_name": information['user']['middle_name'],
                    "phone": information['user']['phone'],
                    "email": information['user']['email'],
                    "company_data": information['user']['company_data'],
                },

                "dinners": {
                    "id": information['id'],
                    "dinner_to_dish": information['dinner_to_dish'],
                    "date_action_begin": information['date_action_begin'],
                    "status": information['status'],
                    "status_name": information['status_name'],
                    "full_cost": information['full_cost'],
                    "oversupply_tariff": information['oversupply_tariff'],
                },

                "full_cost": data['full_cost'],
                "dinners_oversupply_tariff": data.get('dinners_oversupply_tariff'),
                "send_iiko": data['send_iiko'],
            })

    company_structure['full_oversupply_tariff'] = full_oversupply_tariff

    return company_structure


def create_structure_by_dishes(serializer_data):
    # Function to create the structure of dishes, we get the name of the dishes and their quantity

    full_dishes = dict()

    for dinner in serializer_data:
        for dishes in dinner['dinner_to_dish']:
            dish_name = dishes['dish']['name']
            dish_count = dishes['count_dish']

            if not full_dishes.get(dish_name):
                full_dishes.update({
                    dish_name: dish_count,
                })

            else:
                full_dishes[dish_name] += 1

    return full_dishes
