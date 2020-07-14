from django.contrib.auth.models import AbstractUser
from django.db.models import *


class Company(Model):
    company_name = CharField(max_length=20, null=True, blank=True, verbose_name='Название компании')
    full_address = CharField(max_length=500, null=True, blank=True, verbose_name='Полный адрес')
    legal_address = CharField(max_length=500, null=True, blank=True, verbose_name='Юридический адрес')

    general_director = CharField(max_length=45, null=True, blank=True, verbose_name='Генеральный директор')

    inn = CharField(max_length=12, null=True, blank=True, verbose_name='ИНН')
    kpp = CharField(max_length=9, null=True, blank=True, verbose_name='КПП')
    ogrn = CharField(max_length=9, null=True, blank=True, verbose_name='ОГРН')

    registration_date = DateField(null=True, blank=True, verbose_name='Дата регистрации')
    bank_name = CharField(max_length=40, null=True, blank=True, verbose_name='Название банка')
    bik = CharField(max_length=9, null=True, blank=True, verbose_name='БИК')

    corporate_account = CharField(max_length=20, null=True, blank=True, verbose_name='Корпоративный счет')
    settlement_account = CharField(max_length=20, null=True, blank=True, verbose_name='Расчетный счет')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компания'


class Department(Model):
    name = CharField(max_length=20, null=True, blank=True, verbose_name='Название')
    company = ForeignKey('company.Company', on_delete=PROTECT, related_name='company_department', blank=True,
                         null=True, verbose_name='Компания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департамент'
