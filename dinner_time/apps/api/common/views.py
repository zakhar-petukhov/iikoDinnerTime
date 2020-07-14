from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import pagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.common.models import Image
from api.common.serializers import *


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Все настройки.',
    responses={
        '201': openapi.Response('Успешно', SettingsSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление настройки.',
    request_body=SettingsSerializer,
    responses={
        '201': openapi.Response('Успешно', SettingsSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class SettingsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    pagination_class = pagination.LimitOffsetPagination


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание фотографии.',
    operation_description='''
Метод позволяет:
1) прикрепить фотографию к блюду / комплексному обеду.
2) установить аватарку.

ps: У каждого блюда и аватарки по 1 фотографии. Не надо создавать фотографию, если уже есть,
берем "id" фотографии и переходим в update, чтобы поменять, а не создать.
''',
    responses={
        '201': openapi.Response('Создано', ImagesSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление фотографии.',
    responses={
        '202': openapi.Response('Обновлено', ImagesSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр фотографии.',
    responses={
        '200': openapi.Response('Успешно', ImagesSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Удаление фотографии.',
    responses={
        '204': openapi.Response('Не найдено', ImagesSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class ImageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImagesSerializer
    parser_classes = [FormParser, MultiPartParser]
