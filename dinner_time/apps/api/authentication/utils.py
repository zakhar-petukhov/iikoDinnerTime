from django.db.models import Q
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException
from rest_framework import serializers

from apps.api.common.models import ReferralLink
from apps.api.company.utils import send_message
from apps.api.users.models import User
from apps.api.users.utils import create_ref_link_for_update_auth_data


def get_and_authenticate_user(password, username=None):
    auth = CustomAuthenticationBackend()
    user = auth.authenticate(email_or_phone=username, password=password)
    if user is None:
        raise serializers.ValidationError("Некорректные учётные данные. Пожалуйста, попробуйте ещё раз")

    return user


def create_upid_send_message(email):
    user = User.objects.filter(email=email)
    if not user.exists():
        return serializers.ValidationError("Введите правильный адрес почты")

    referral_link = ReferralLink.objects.filter(user=user.first())

    if not referral_link.exists():
        link = create_ref_link_for_update_auth_data(obj=user.first())
    else:
        referral_link = referral_link.first()
        referral_link.upid = ReferralLink.get_generate_upid()
        referral_link.save()

        link = referral_link.upid

    user = user.first()
    is_company = True if user.company_data else False

    send_message(company_name=None, upid=link, data={'email': email}, is_company=is_company,
                 is_recovery_password=True)


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
