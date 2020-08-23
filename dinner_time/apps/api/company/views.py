from datetime import datetime

import pytz
from django.conf import settings
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, pagination
from rest_framework import response
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.api.company.data_for_swagger import *
from apps.api.company.filters import OrderDateFilter
from apps.api.company.serializers import *
from apps.api.company.utils import create_user_or_company
from apps.api.dinner.models import Dinner, CompanyOrder
from apps.api.dinner.serializers import DinnerSerializer, DinnerOrderSerializer
from apps.api.users.models import User
from apps.api.users.permissions import IsCompanyAuthenticated
from apps.api.users.serializers import UserCreateSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Создание компании',
    responses={
        '201': openapi.Response('Создано', CompanyCreateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CreateCompanyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CompanyCreateSerializer
    permission_classes = [IsAdminUser]

    # Create company and send message to email manager company for change password
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_name = serializer.data['company_data'].get('company_name')
        return create_user_or_company(company_name=company_name, serializer=serializer, is_company=True)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Просмотр всех компаний',
    operation_description='Просмотр всех компаний. Есть возможность отфильтровать по названию',
    responses={
        '200': openapi.Response('Успешно', CompanyGetSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class AllCompaniesView(ListAPIView):
    queryset = User.objects.filter(company_data__isnull=False, is_active=True)
    serializer_class = CompanyGetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_data__company_name']
    permission_classes = [IsAdminUser]
    pagination_class = pagination.LimitOffsetPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Детальный просмотр одной компании.',
    operation_description='''Есть возможность полностью посмотореть данные о компании \
(сколько человек, какие созданы отделы)''',
    responses={
        '200': openapi.Response('Успешно', CompanyGetSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyDetailView(ListAPIView):
    serializer_class = CompanyGetSerializer
    permission_classes = [IsCompanyAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        return User.objects.filter(id=company_id, company_data__isnull=False)


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary='Обновление данных компании',
    operation_description='''
Можем производить все манипуляции с компанией:
1) Обновление любого поля менеджера компании
2) Обновление любого поля самой компании
3) Блокировка компании {"is_block": true} ---> {"is_block": false}
4) Удаление компании {"is_active": false} - компания переводится в статус неактивна, но из базы данных не удаляется
''',
    request_body=CompanyGetSerializer,
    responses={
        '200': openapi.Response('Успешно', CompanyGetSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyChangeDetailView(UpdateAPIView):
    serializer_class = CompanyGetSerializer
    permission_classes = [IsCompanyAuthenticated]

    def get_object(self):
        company_id = self.kwargs.get("company_id")
        return get_object_or_404(User, id=company_id, company_data__isnull=False)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        company_data = request.data.pop('company_data', None)
        is_blocked = request.data.pop('is_blocked', None)

        if company_data:
            Company.objects.filter(company_user=instance).update(**company_data)

        if is_blocked in [True, False]:
            instance.is_blocked = is_blocked
            instance.block_date = datetime.now(pytz.timezone(settings.TIME_ZONE)) if is_blocked else None
            instance.save()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return response.Response(serializer.data)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание отдела',
    operation_description='''
В поле "company" передаем "id" компании, к которой привязываем этот отдел.
''',
    responses={
        '201': openapi.Response('Создано', DepartmentSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр отделов.',
    operation_description='''
Если передаем "department_id" в заголовке, то нам доступен только один отдел и его сотрудники, если не передаем, \
то получаем все отделы.
''',
    responses={
        '200': openapi.Response('Успешно', DepartmentSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DepartmentViewSet(ModelViewSet):
    permission_classes = [IsCompanyAuthenticated]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        department_id = self.kwargs.get('department_id', None)
        employee_id = self.request.user.id

        if department_id:
            return Department.objects.filter(id=department_id)

        return Department.objects.filter(company_id__company_user=User.objects.get(id=employee_id))


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Добавление сотрудников в отделы',
    operation_description='''Создается сотрудник и добавляется в отдел.
Сотруднику генерируется базовый логин и пароль и отправляется на почту сообщение о смене, после перехода по \
уникальной ссылке, сотрудник ставит свой логин и пароль''',
    responses={
        '202': openapi.Response('Изменено', UserCreateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DepartmentCreateUserViewSet(ModelViewSet):
    permission_classes = [IsCompanyAuthenticated]
    serializer_class = UserCreateSerializer

    # Create, add user into department and send message for change password, and login on the mail
    def create(self, request, *args, **kwargs):
        parent = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return create_user_or_company(company_name=parent.company_data.company_name, serializer=serializer,
                                      parent=parent)


@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление заказа сотрудника.',
    operation_description='''
Имеем 4 статуса заказа:
1) В обработке (дефолт)
2) Принят
3) Отменен
4) Подтвержден ---> можем отправлять админу в privet-obed, а после на кухню
''',
    request_body=request_for_update_employee_order,
    responses={
        '200': openapi.Response('Успешно', DinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр заказов от сотрудников.',
    operation_description='''
При передаче user_id сотрудника покажется заказы только этого сотрудника.
Можно использовать фильтры:
date_action_begin__lte - с какого числа
date_action_begin__gte - по какое число
''',
    responses={
        '200': openapi.Response('Успешно', DinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DinnerCheckOrderViewSet(ModelViewSet):
    permission_classes = [IsCompanyAuthenticated]
    serializer_class = DinnerSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = OrderDateFilter

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        company_id = self.request.user

        if user_id:
            return Dinner.objects.filter(user_id=user_id).order_by('-id')

        if not company_id.is_anonymous:
            return Dinner.objects.filter(company_id=company_id.company_data.id).order_by('-id')

    def list(self, request, *args, **kwargs):
        serializer_data = super().list(request, *args, **kwargs).data
        month_oversupply_tariff = 0
        for oversupply_tariff in serializer_data:
            month_oversupply_tariff += oversupply_tariff['oversupply_tariff']

        serializer_data.append({'month_oversupply_tariff': month_oversupply_tariff})

        custom_data = {'month_oversupply_tariff': month_oversupply_tariff, "data": serializer_data}

        return response.Response(custom_data)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание заказа от компании',
    operation_description='''Создается заказ, который отправляется к администратору privet-obed.
Принимаются заказы только со статусом "Подтвержден"''',
    request_body=request_for_create_order,
    responses={
        '201': openapi.Response('Создано', DinnerOrderSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр историй заказов.',
    operation_description='''Есть возможность просмотра всех заказов компании, а также посмотреть детально \
только один заказ, путем передачи order_id.''',
    responses={
        '200': openapi.Response('Успешно', DinnerOrderSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyOrderView(ModelViewSet):
    serializer_class = DinnerOrderSerializer
    permission_classes = [IsCompanyAuthenticated]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):  # TODO: сделать отдельно админку и не городить все в один запрос, нарушает принцип SOLID
        is_superuser = self.request.user.is_superuser
        order_id = self.kwargs.get('order_id', None)

        if is_superuser:
            if order_id:
                return CompanyOrder.objects.filter(id=order_id).order_by('-id')

            return CompanyOrder.objects.all().order_by('-id')

        else:
            company_id = self.request.user.id
            if order_id:
                return CompanyOrder.objects.filter(id=order_id, company__id=company_id).order_by('-id')

            return CompanyOrder.objects.filter(company__id=company_id).order_by('-id')
