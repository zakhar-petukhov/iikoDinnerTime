import uuid

from django.contrib.auth import get_user_model

from apps.api.common.models import ReferralLink
from apps.api.company.models import Company


def generate_random_password_username():
    return {
        'username': uuid.uuid4().hex[:15],
        'password': uuid.uuid4().hex[:30]
    }


def create_ref_link_for_update_auth_data(obj):
    link = ReferralLink.objects.create(user=obj, upid=ReferralLink.get_generate_upid())
    return link.upid


def create_user_account(email, first_name="", last_name="", parent=None, **extra_fields):
    company_data = extra_fields.get('company_data')

    if company_data:
        company = Company.objects.create(**company_data)
        extra_fields['company_data'] = company

    user = get_user_model().objects.create_user(
        email=email, first_name=first_name, last_name=last_name, parent=parent, **extra_fields)
    return user
