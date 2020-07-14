from django.http import HttpResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.company.utils import send_message
from api.dinner.data_for_swagger import request_for_create_dinner
from api.dinner.models import Dinner
from api.dinner.serializers import DinnerSerializer
from api.users.data_for_swagger import request_invite_users, request_for_change_user_information
from api.users.permissions import IsCompanyAuthenticated
from api.users.serializers import *
from api.users.utils import *

User = get_user_model()


@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Изменение информации о сотруднике',
    operation_description='Только менеджер компании может менять информацию о сотруднике',
    request_body=request_for_change_user_information,
    responses={
        '200': openapi.Response('Успешно', UserSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Детальный просмотр одного сотрудника',
    operation_description='Сотрудник может посмотреть всю информацию о себе',
    responses={
        '200': openapi.Response('Успешно', UserSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class UserView(ModelViewSet):
    permission_classes = [IsCompanyAuthenticated, ]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get("pk"))

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return get_object_or_404(User, id=user_id)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание обеда',
    request_body=request_for_create_dinner,
    responses={
        '201': openapi.Response('Создано', DinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class UserCreateDinnerView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Dinner.objects.all()
    serializer_class = DinnerSerializer

    def get_object(self):
        return get_object_or_404(Dinner, id=self.kwargs.get("dish_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Все доступные тарифы.',
    responses={
        '200': openapi.Response('Успешно', TariffSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Изменение тарифа.',
    responses={
        '200': openapi.Response('Успешно.', TariffSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание тарифа.',
    request_body=TariffSerializer,
    responses={
        '201': openapi.Response('Создано', TariffSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class TariffCreateView(ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Tariff, id=self.kwargs.get("tariff_id"))


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Приглашение работников от имени компании.',
    request_body=request_invite_users,
    responses={
        '201': openapi.Response('Создано'),
        '400': 'Неверный формат запроса'
    }
)
                  )
class InviteUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form_data = request.data

        tariff = form_data.pop('tariff')
        parent = request.user

        for employee in form_data['emails']:
            employee['tariff'] = Tariff.objects.get(pk=tariff)
            employee.update(generate_random_password_username())
            user = create_user_account(parent=parent, **employee)
            upid = create_ref_link_for_update_auth_data(obj=user)
            send_message(company_name=parent.company_data.company_name, upid=upid, data=employee, is_company=False)

        return HttpResponse(status=status.HTTP_201_CREATED)
