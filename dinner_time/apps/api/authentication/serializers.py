from django.contrib.auth import password_validation
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.api.users.models import User


class UserLoginSerializer(serializers.Serializer):
    """
    A user serializer for login the user
    """

    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    """
    A user serializer for authentication the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token, create = Token.objects.get_or_create(user=obj)
        return token.key


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
