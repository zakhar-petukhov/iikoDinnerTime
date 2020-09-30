from django.contrib.auth.models import AbstractUser
from django.db.models import *


class Company(Model):
    company_name = CharField(max_length=20, null=True, blank=True, verbose_name='Название компании')

    city = CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    street = CharField(max_length=100, null=True, blank=True, verbose_name='Улица')
    house = CharField(max_length=30, null=True, blank=True, verbose_name='Номер дома')
    house_building = CharField(max_length=30, null=True, blank=True, verbose_name='Корпус дома')
    apartment = CharField(max_length=30, null=True, blank=True, verbose_name='Номер квартиры')

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

    def get_full_address(self):
        full_address = f"{self.city}, {self.street}, {self.house}, {self.apartment}"
        return full_address.strip()

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компания'


class Address(Model):
    company = ForeignKey('company.Company', on_delete=PROTECT, related_name='company_address', blank=True,
                         null=True, verbose_name='Компания')

    city = CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    street = CharField(max_length=100, null=True, blank=True, verbose_name='Улица')
    house = CharField(max_length=30, null=True, blank=True, verbose_name='Номер дома')
    house_building = CharField(max_length=30, null=True, blank=True, verbose_name='Корпус дома')
    apartment = CharField(max_length=30, null=True, blank=True, verbose_name='Номер квартиры')

    def __str__(self):
        return f"Город {self.city}, улица {self.street}, дом {self.house}, квартира {self.apartment}"

    @property
    def full_address(self):
        return f"Город {self.city}, улица {self.street}, дом {self.house}, \
{f'корпус {self.house_building}, квартира {self.apartment}' if self.house_building else self.apartment}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адрес'
