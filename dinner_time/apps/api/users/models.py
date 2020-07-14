from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import *
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser, MPTTModel):
    objects = UserManager()

    parent = TreeForeignKey('self', on_delete=CASCADE, verbose_name='Куратор', null=True, blank=True,
                            related_name='childs')

    first_name = CharField(max_length=20, null=True, blank=True, verbose_name='Имя')
    last_name = CharField(max_length=20, null=True, blank=True, verbose_name='Фамилия')
    middle_name = CharField(max_length=20, null=True, blank=True, verbose_name='Отчество')

    phone = PhoneNumberField(null=True, blank=True, unique=True, region='RU', verbose_name='Номер телефона')
    email = EmailField(max_length=30, null=True, blank=True, verbose_name='Email')
    email_verified = BooleanField(default=False, verbose_name='Email подтвержден')

    tariff = ForeignKey('users.Tariff', on_delete=PROTECT, related_name='tariff_user', blank=True,
                        null=True, verbose_name='Тариф')

    department = ForeignKey('company.Department', on_delete=PROTECT, related_name='department_user', blank=True,
                            null=True, verbose_name='Департамент')

    is_blocked = BooleanField(default=False, verbose_name='Заблокирован')
    block_date = DateTimeField(null=True, blank=True, verbose_name='Дата блокироваки')

    company_data = OneToOneField('company.Company', on_delete=PROTECT, null=True, blank=True,
                                 related_name='company_user', verbose_name='Компания')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    update_date = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocked = self.is_blocked

    def save(self, *args, **kwargs):
        if self.is_blocked and not self.blocked:
            self.block_date = datetime.now(pytz.timezone(settings.TIME_ZONE))
        else:
            self.block_date = None

        return super().save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
        return 'id', 'username', 'last_name', 'first_name', 'phone'

    @property
    def is_company(self):
        if self.company_data:
            return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tariff(Model):
    name = CharField(max_length=20, null=True, blank=True, verbose_name='Название')
    max_cost_day = IntegerField(null=True, blank=True, verbose_name='Дневная сумма заказа')
    description = CharField(max_length=130, null=True, blank=True, verbose_name='Описание')
    is_blocked = BooleanField(default=False, verbose_name='Заблокирован')
