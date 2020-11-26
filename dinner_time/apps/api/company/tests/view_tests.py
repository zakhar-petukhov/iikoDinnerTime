import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCompanyView:
    def test_company_create(self, api_client, token_user):
        url = reverse('COMPANY:create_company')
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "company_data": {
                "company_name": "ООО Тест",
                "city": "Санкт-Петербург",
                "street": "Невский проспект",
                "house": "5",
                "registration_date": "2020-04-25"
            },
            "first_name": "Тест",
            "last_name": "Тестов",
            "middle_name": "Тестович",
            "phone": "89313123445",
            "email": "test_company@mail.ru"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_list_all_company(self, api_client, token_user):
        url = reverse('COMPANY:all_companies')
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(path=url)
        company_data = json.loads(response.content)

        assert response.status_code == 200
        assert company_data[0]['company_data']['company_name'] == "ООО Тест"
        assert company_data[0]['first_name'] == "Тест"

    def test_list_detail_company(self, api_client, token_user, company):
        company = company
        url = reverse('COMPANY:detail_company', kwargs={'company_id': company.id})
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(path=url)
        company_data = json.loads(response.content)

        assert response.status_code == 200
        assert company_data[0]['company_data']['company_name'] == "ООО Тест"
        assert company_data[0]['first_name'] == "Тест"

    def test_change_detail_company(self, api_client, token_user, company):
        company = company
        url = reverse('COMPANY:change_detail_company', kwargs={'company_id': company.id})
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "company_data": {
                "company_name": "ООО Тестик",
            },
            "is_blocked": True,
            "is_active": False
        }

        response = api_client.put(path=url, data=data)
        company_data = json.loads(response.content)

        assert response.status_code == 200
        assert company_data['company_data']['company_name'] == "ООО Тестик"
        assert company_data['is_blocked'] is True


@pytest.mark.django_db
class TestDepartmentView:
    def test_group_create(self, api_client, token_company, tariff):
        token, company = token_company
        url = reverse('USERS:user_group-list')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {
            "name": "IT отдел",
            "tariff": tariff.id
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_list_all_group(self, api_client, token_company, group):
        token, company = token_company
        url = reverse('USERS:user_group-list')
        group()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = api_client.get(path=url)
        group_response = json.loads(response.content)

        assert response.status_code == 200
        assert group_response[0]['name'] == "Айтишники"

    def test_add_employee_into_group(self, api_client, token_company, group):
        token, company = token_company
        url = reverse('COMPANY:department_add_user')
        group()

        data = {
            "first_name": "Тест",
            "last_name": "Тестов",
            "middle_name": "Тестович",
            "phone": "89313123332",
            "email": "test_company@mail.ru",
        }

        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_list_detail_group(self, api_client, token_company, group):
        url = reverse('USERS:user_group-detail', kwargs={'pk': group().id})
        token, company = token_company
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = api_client.get(path=url)
        group_response = json.loads(response.content)

        assert response.status_code == 200
        assert group_response['name'] == "Айтишники"

    def test_get_company_history_order(self, api_client, token_company):
        token, company = token_company
        url = reverse('COMPANY:company_history_order')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(path=url)

        assert response.status_code == 200

    def test_get_check_employee_order(self, api_client, token_company):
        token, company = token_company
        url = reverse('COMPANY:check_employee_order')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(path=url)

        assert response.status_code == 200

    def test_get_detail_order(self, api_client, token_company, company_order):
        token, company = token_company
        url = reverse('COMPANY:company_history_order_detail', kwargs={'order_id': company_order().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(path=url)
        order_data = json.loads(response.content)

        assert response.status_code == 200
        assert order_data[0]['company']['company_data']['company_name'] == 'ООО Тест'

    def test_create_order(self, api_client, token_company, company_order):
        token, company = token_company
        url = reverse('COMPANY:send_employee_order_to_admin')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        success_data = {
            "dinners": [
                {
                    "id": company_order(status=3).id
                }
            ]
        }

        data_with_status_error = {
            "dinners": [
                {
                    "id": company_order().id
                }
            ]
        }

        data_with_id_error = {
            "dinners": [
                {
                    "id": 24
                }
            ]
        }

        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = api_client.post(url, data=json.dumps(success_data), content_type='application/json')
        assert response.status_code == 201

        response = api_client.post(url, data=json.dumps(data_with_status_error), content_type='application/json')
        req_data = json.loads(response.content)

        assert response.status_code == 400
        assert req_data['error_text'] == 'Статус заказа должен быть "Подтвержден"'

        response = api_client.post(url, data=json.dumps(data_with_id_error), content_type='application/json')
        req_data = json.loads(response.content)

        assert response.status_code == 400
        assert req_data['error_text'] == "Такого id заказа не существует"
