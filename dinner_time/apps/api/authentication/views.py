from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.common.models import ReferralLink
from apps.api.users.serializers import EmptySerializer
from .serializers import *
from .utils import create_upid_send_message


@method_decorator(name='login', decorator=swagger_auto_schema(
    operation_summary='Аутентификация и авторизация',
    responses={
        '200': openapi.Response('Успешно', AuthUserSerializer),
        '400': 'Неверный формат запроса'
    }
)

                  )
@method_decorator(name='logout', decorator=swagger_auto_schema(
    operation_summary='Выход из системы',
    responses={
        '200': openapi.Response('Успешный выход из системы'),
        '400': 'Неверный формат запроса'
    }
)

                  )
@method_decorator(name='password_change', decorator=swagger_auto_schema(
    operation_description='Пользоваель вводит существующий и новый пароль',
    operation_summary='Смена пароля',
    responses={
        '202': openapi.Response('Успешно'),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='password_reset', decorator=swagger_auto_schema(
    operation_description='Пользоваель вводит существующий и новый пароль',
    operation_summary='Смена пароля',
    responses={
        '202': openapi.Response('Успешно'),
        '400': 'Неверный формат запроса'
    }
)
                  )
class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': AuthUserSerializer,
        'password_change': PasswordChangeSerializer,
        'password_reset': RecoveryPasswordSerializer,
    }

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        user = getattr(request, 'user', None)
        Token.objects.get(user=user).delete()
        logout(request)
        return Response(data='Успешный выход из системы', status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['PUT'], detail=False, permission_classes=[])
    def password_reset(self, request):
        email = request.data.get('email')
        upid = request.data.get('upid')
        password = request.data.get('password')

        if email:
            create_upid_send_message(email)

        elif upid:
            user = get_object_or_404(User, ref_link__upid=upid, ref_link__is_active=True)
            user.set_password(password)
            user.ref_link.update(is_active=False)
            user.save()

        return Response(status=status.HTTP_202_ACCEPTED)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary='Смена пароля компании / сотрудника',
    operation_description='''Администратор добавляет через свою панель компанию, на ее почту приходит письмо с ссылкой \
для смены пароля.
Компания, в свою очередь, может добавить сотрудника в свой отдел и ему приходит тоже письмо о смене пароля.''',
    responses={
        '200': openapi.Response('Успешно', PasswordChangeSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class UserChangeRegAuthDataView(UpdateAPIView):
    serializer_class = ChangeRegAuthDataSerializer
    model = User
    permission_classes = ()

    def get_object(self):
        upid = self.kwargs["referral_upid"]
        obj = get_object_or_404(ReferralLink, upid=upid, is_active=True)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.is_active = False
        instance.user.set_password(request.data.get("password"))
        request.data['password'] = instance.user.password

        serializer = self.get_serializer(instance.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, instance)
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer, instance):
        serializer.save()
        instance.save()
