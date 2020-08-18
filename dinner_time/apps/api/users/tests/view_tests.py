import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserView:
    def test_user_change_information(self, api_client, get_token_user, get_token_company):
        token_company, company = get_token_company
        token_user, user = get_token_user
        url = reverse('USERS:change_detail_information', kwargs={'pk': user.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "first_name": "Пупкин",
            "is_blocked": True
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 200
        user_data['first_name'] = 'Пупкин'
        user_data['is_blocked'] = True

    def test_user_get_detail_information(self, api_client, get_token_user):
        token_user, user = get_token_user
        url = reverse('USERS:detail_information', kwargs={"pk": user.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data[0]['first_name'] == 'Тест'

    def test_create_tariff(self, api_client, get_token_user):
        token_user, user = get_token_user
        url = reverse('USERS:group_tariff-list')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "name": "Лайт",
            "max_cost_day": 300,
            "description": "Тупа чтобы шашлыка навернуть"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        assert user_data['name'] == 'Лайт'

    def test_change_tariff(self, api_client, get_token_user, create_tariff):
        token_user, user = get_token_user
        url = reverse('USERS:group_tariff-detail', kwargs={"pk": create_tariff().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "max_cost_day": 500
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data['max_cost_day'] == 500

    def test_get_all_tariff(self, api_client, get_token_user, create_tariff, ):
        create_tariff()
        token_user, user = get_token_user
        url = reverse('USERS:group_tariff-list')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data[0]['name'] == "Лайт"

    def test_invite_users(self, api_client, get_token_company, create_tariff, create_group):
        token_company, company = get_token_company
        url = reverse('USERS:invite_user')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "tariff": create_tariff().id,
            "group": create_group().id,
            "emails": [
                {
                    "email": "zakharpetukhov@protonmail.com"
                },
                {
                    "email": "zakharpetukhov01@gmail.com"
                }
            ]
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_change_data_with_referral_upid(self, api_client, create_referral_upid):
        url = reverse('USERS:user_change_auth_ref', kwargs={"referral_upid": create_referral_upid()})

        data = {
            "password": "TEST",
            "phone": 89313149331,
            "email_verified": True
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 200

    def test_user_create_dinner(self, api_client, get_token_user, create_dish):
        token, user = get_token_user
        dish_id = create_dish().id
        url = reverse('USERS:user_add_dish')

        data = {
            "dishes": [
                {
                    "id": dish_id
                }
            ]
        }

        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        assert user_data['dinner_to_dish'][0]['dish']['name'] == 'Томатный суп'
