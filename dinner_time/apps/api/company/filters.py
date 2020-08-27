import django_filters
from django.db import models as django_models

from apps.api.dinner.models import Dinner, CompanyOrder


class DateFilter(django_filters.rest_framework.FilterSet):
    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }


class UserOrderDateFilter(DateFilter):
    class Meta:
        model = Dinner
        fields = {
            'date_action_begin': ('gte', 'lte')
        }


class CompanyOrderDateFilter(DateFilter):
    class Meta:
        model = CompanyOrder
        fields = {
            'create_date': ('gte', 'lte')
        }
