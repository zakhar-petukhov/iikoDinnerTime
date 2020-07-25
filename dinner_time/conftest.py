import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.api.common.models import Settings
from apps.api.company.models import Company, Department
from apps.api.dinner.models import CategoryDish, Dish, DayMenu, Dinner, CompanyOrder, Template, WeekMenu
from apps.api.users.models import User, Tariff
from apps.api.users.utils import create_ref_link_for_update_auth_data


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_company(db, django_user_model):
    def make_company():
        data = {
            "company_data": {
                "company_name": "ООО Тест",
                "full_address": "ул. Пушкина, дом Колотушкина",
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

        company_data = data['company_data']
        company, _ = Company.objects.get_or_create(**company_data)
        data['company_data'] = company
        manager_with_company, _ = User.objects.get_or_create(**data)
        return manager_with_company

    return make_company


@pytest.fixture
def create_department(db, django_user_model, get_token_company):
    def make_department():
        token, company = get_token_company
        data = {
            "name": "Любители вкусняшек",
            "company": company.company_data
        }

        return Department.objects.create(**data)

    return make_department


@pytest.fixture
def create_category_dish(django_user_model, get_token_company):
    def make_category_dish():
        data = {
            "name": "Первые блюда"
        }

        return CategoryDish.objects.create(**data)

    return make_category_dish


@pytest.fixture
def create_dish(django_user_model, get_token_company, create_category_dish):
    def make_dish():
        data = {
            "name": "Томатный суп",
            "cost": 90,
            "weight": 120,
            "description": "Томат, горох",
            "category_dish": create_category_dish()
        }

        return Dish.objects.create(**data)

    return make_dish


@pytest.fixture
def create_complex_dish(django_user_model, get_token_company, create_dish):
    def make_complex_dish():
        data = {
            "name": "Комплексный обед №1",
            "cost": 160
        }

        Settings.objects.create()  # create the settings to take effect
        complex_dinner = Dish.objects.create(**data)
        complex_dinner.added_dish.add(create_dish())

        return complex_dinner

    return make_complex_dish


@pytest.fixture
def create_tariff(django_user_model, get_token_user):
    def make_tariff():
        data = {
            "name": "Лайт",
            "max_cost_day": 300,
            "description": "Тупа чтобы шашлыка навернуть"
        }

        return Tariff.objects.create(**data)

    return make_tariff


@pytest.fixture
def create_menu(django_user_model, get_token_company, create_dish):
    def make_menu():
        day_menu = DayMenu.objects.create()
        day_menu.dish.add(create_dish())

        return day_menu

    return make_menu


@pytest.fixture
def get_token_user(db, create_user, create_company):
    user = create_user(phone='89313147222', first_name='Тест', last_name="Тестовов",
                       email='test@protonmail.com', username='test', password='test', is_superuser=True,
                       is_staff=True)
    token, _ = Token.objects.get_or_create(user=user)
    return token, user


@pytest.fixture
def get_token_company(db, create_company):
    company = create_company()
    token, _ = Token.objects.get_or_create(user=company)
    return token, company


@pytest.fixture
def create_company_order(db, get_token_company, get_token_user, create_dish):
    def make_order():
        token, company = get_token_company
        token, user = get_token_user
        dish = create_dish()
        dinner = Dinner.objects.create(user=user, company=company.company_data)
        dinner.dishes.add(dish)

        company_order = CompanyOrder.objects.create(company=company)
        company_order.dinners.add(dinner)

        return company_order

    return make_order


@pytest.fixture
def create_referral_upid(db, get_token_user):
    def make_referral_upid():
        token, user = get_token_user
        upid = create_ref_link_for_update_auth_data(obj=user)

        return upid

    return make_referral_upid


@pytest.fixture
def create_week_menu(db, create_menu):
    def make_create_week_menu():
        week_menu = WeekMenu.objects.create()
        week_menu.dishes.add(create_menu())
        return week_menu

    return make_create_week_menu


@pytest.fixture
def create_template(db, create_week_menu):
    def make_create_template():
        data = {
            "name": "Шаблон №0",
            "number_week": 1
        }

        return Template.objects.create(menu=create_week_menu(), **data)

    return make_create_template
