from django.contrib.auth.models import User
from django.db.models import Q
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException
from rest_framework import serializers

from api.users.models import User


def get_and_authenticate_user(password, username=None):
    auth = CustomAuthenticationBackend()
    user = auth.authenticate(email_or_phone=username, password=password)
    if user is None:
        raise serializers.ValidationError("Некорректные учётные данные. Пожалуйста, попробуйте ещё раз")

    return user


class CustomAuthenticationBackend:
    def authenticate(self, email_or_phone=None, password=None):
        try:
            email_or_phone = self.get_username(email_or_phone)

            user = User.objects.get(
                Q(email=email_or_phone) | Q(phone=email_or_phone)
            )
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_username(self, email_or_phone):
        try:
            email_or_phone = PhoneNumber.from_string(phone_number=email_or_phone, region='RU').as_e164
            return email_or_phone

        except NumberParseException:
            return email_or_phone
