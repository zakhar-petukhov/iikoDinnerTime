from apps.api.dinner.models import CompanyOrder
from iiko import data_getters
from iiko.api import IikoService


def create_order(request, company_order_id):
    company_order = CompanyOrder.objects.filter(id=company_order_id).first()
    try:
        data_send_dishes = data_getters.send_dishes_data(company_order)

        iiko_service = IikoService()
        iiko_service.create_company_order(data_send_dishes)

        return {
            'error': False,
            'content': {
                'status': "Заказ успешно создан"
            },
            'error_text': None
        }

    except Exception:  # TODO: сделать логи
        return {
            'error': True,
            'content': {
                'status': "Произошла ошибка при создании заказа"
            },
            'error_text': None
        }
