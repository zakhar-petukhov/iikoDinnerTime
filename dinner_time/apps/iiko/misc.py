from sentry_sdk import capture_exception

from apps.api.dinner.models import CompanyOrder
from apps.iiko import data_getters
from apps.iiko.api import IikoService


def create_order(request, company_order_id):
    STATUS_ERROR = "Произошла ошибка при создании заказа"

    company_order = CompanyOrder.objects.filter(id=company_order_id, send_iiko=False).first()

    try:
        if not company_order:
            STATUS_ERROR = "Заказ уже был отправлен в iiko, повторная отправка невозможна"
            raise Exception(STATUS_ERROR)

        data_send_dishes = data_getters.send_dishes_data(company_order)

        iiko_service = IikoService()
        iiko_service.create_company_order(data_send_dishes)

        company_order.send_iiko = True
        company_order.save()

        return {
            'error': False,
            'content': {
                'status': "Заказ успешно создан"
            },
            'error_text': None
        }

    except Exception as exception:
        capture_exception(exception)

        return {
            'error': True,
            'content': {
                'status': STATUS_ERROR
            },
            'error_text': None
        }
