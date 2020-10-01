from datetime import datetime, timedelta

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.api.common.models import Settings
from apps.api.company.models import Company, DeliveryAddress
from apps.api.dinner.models import CategoryDish, Dish, DayMenu, Dinner, CompanyOrder, WeekMenu, DinnerDish
from apps.api.users.models import User, Tariff, CustomGroup
from apps.api.users.utils import create_ref_link_for_update_auth_data


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def token_user(db, django_user_model, group):
    user = django_user_model.objects.create_user(phone='89313147222', first_name='Тест', last_name="Тестовов",
                                                 email='test@protonmail.com', username='test', password='test',
                                                 is_superuser=True, is_staff=True, group=group())
    token, _ = Token.objects.get_or_create(user=user)
    return token, user


@pytest.fixture
def token_company(db, company):
    company = company
    token, _ = Token.objects.get_or_create(user=company)
    return token, company


@pytest.fixture
def group(db, tariff, token_company):
    def make_group():
        token, company = token_company

        delivery_address = DeliveryAddress.objects.create(**{
            "city": "Санкт-Петербург",
            "street": "Пушкина",
            "house": "3",
            "house_building": "1",
            "apartment": "120",
        })

        return CustomGroup.objects.create(**{
            "name": "Айтишники",
            "tariff": tariff,
            "company": company.company_data,
            "address_for_delivery": delivery_address
        })

    return make_group


@pytest.fixture
def tariff(db, token_company):
    token, company = token_company

    data = {
        "name": "Лайт",
        "max_cost_day": 300,
        "company": company.company_data,
        "description": "Тупа чтобы шашлыка навернуть"
    }
    tariff, _ = Tariff.objects.get_or_create(**data)

    return tariff


@pytest.fixture
def company(db, django_user_model):
    data = {
        "company_data": {
            "company_name": "ООО Тест",
            "city": "Санкт-Петербург",
            "street": "Пушкина",
            "house": "3",
            "house_building": "1",
            "apartment": "120",
            "registration_date": "2020-04-25"
        },
        "first_name": "Тест",
        "last_name": "Тестов",
        "middle_name": "Тестович",
        "phone": "89313123442",
        "email": "test_company@mail.ru",
        "username": "test_company",
        "password": 'test_company',
    }

    company, _ = Company.objects.get_or_create(**data['company_data'])
    data['company_data'] = company
    manager_with_company, _ = User.objects.get_or_create(**data)

    return manager_with_company


@pytest.fixture
def category_dish(django_user_model, token_company):
    def make_category_dish():
        return CategoryDish.objects.create(**{
            "name": "Первые блюда"
        })

    return make_category_dish


@pytest.fixture
def second_category_dish(django_user_model, token_company):
    def make_category_dish():
        return CategoryDish.objects.create(**{
            "name": "Вторые блюда"
        })

    return make_category_dish


@pytest.fixture
def dish(django_user_model, token_company, category_dish):
    def make_dish():
        return Dish.objects.create(**{
            "name": "Томатный суп",
            "cost": 90,
            "weight": 120,
            "description": "Томат, горох",
            "category_dish": category_dish()
        })

    return make_dish


@pytest.fixture
def complex_dish(django_user_model, token_company, dish):
    def make_complex_dish():
        Settings.objects.create()  # create the settings to take effect
        complex_dinner = Dish.objects.create(**{
            "name": "Комплексный обед №1",
            "cost": 160
        })
        complex_dinner.added_dish.add(dish())

        return complex_dinner

    return make_complex_dish


@pytest.fixture
def menu(django_user_model, token_company, dish):
    def make_menu():
        day_menu = DayMenu.objects.create()
        day_menu.dish.add(dish())

        return day_menu

    return make_menu


@pytest.fixture
def company_order(db, token_company, token_user, dish):
    def make_order(status=1):
        token, company = token_company
        token, user = token_user
        dinner = Dinner.objects.create(user=user, company=company.company_data, status=status,
                                       date_action_begin='2020-08-31')
        DinnerDish.objects.create(dish=dish(), dinner=dinner, count_dish=3)
        company_order = CompanyOrder.objects.create(company=company)
        company_order.dinners.add(dinner)

        return company_order

    return make_order


@pytest.fixture
def referral_upid(db, token_user):
    def make_referral_upid():
        token, user = token_user
        upid = create_ref_link_for_update_auth_data(obj=user)

        return upid

    return make_referral_upid


@pytest.fixture
def week_menu(db, menu):
    def make_week_menu():
        start_menu = datetime.now() - timedelta(days=5)
        close_menu = datetime.now() + timedelta(days=5)

        week_menu = WeekMenu.objects.create(name='Первая неделя',
                                            start_menu=start_menu.strftime("%Y-%m-%d"),
                                            close_menu=close_menu.strftime("%Y-%m-%d")
                                            )
        week_menu.dishes.add(menu())
        return week_menu

    return make_week_menu
