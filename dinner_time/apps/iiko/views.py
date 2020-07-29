from django.http import JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from iiko.misc import create_order


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Выгрузка блюд в iiko.',
    operation_description='''Метод для выгрузки блюд в iiko, передаем в url "company_order_id", который получили 
из запроса "/company/history/order/".''',
    responses={
        '200': openapi.Response('Успешно'),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CreateOrder(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, company_order_id):
        result = create_order(request, company_order_id)

        if result['error']:
            return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(result, status=status.HTTP_200_OK)
