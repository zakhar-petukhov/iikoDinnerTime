import django_filters
from django.db import models as django_models

from apps.api.dinner.models import Dinner


class OrderDateFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Dinner
        fields = {
            'date_action_begin': ('lte', 'gte')
        }

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }
