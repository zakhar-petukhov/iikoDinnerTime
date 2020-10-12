from django.contrib.auth import password_validation
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.api.authentication.utils import get_and_authenticate_user
from apps.api.users.models import User


class AuthUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=20, read_only=True)
    last_name = serializers.CharField(max_length=20, read_only=True)
    middle_name = serializers.CharField(max_length=20, read_only=True)

    auth_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def validate(self, data):
        """
        Validates user data.
        """
        username = data.get('username', None)
        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'Для входа в систему требуется пароль'
            )

        user = get_and_authenticate_user(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким юзернеймом и паролем не найден'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Этот пользователь был деактивирован'
            )

        if user.is_blocked:
            raise serializers.ValidationError(
                'Этот пользователь был заблокирован'
            )

        token, create = Token.objects.get_or_create(user=user)

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'auth_token': token.key
        }


class PasswordChangeSerializer(serializers.Serializer):
    """
    A user serializer for change password
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Текущий пароль не совпадает')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class RecoveryPasswordSerializer(serializers.Serializer):
    """
    A user serializer for recovery password
    """
    email = serializers.CharField()
    password = serializers.CharField()
    upid = serializers.CharField()


class ChangeRegAuthDataSerializer(serializers.ModelSerializer):
    """
    A serializer for update password when clicking on the registration link
    """

    password = serializers.CharField(required=True)
    phone = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    def validate_phone(self, value):
        phone = PhoneNumber.from_string(phone_number=value, region='RU').as_e164
        return phone

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'password', 'email_verified')
