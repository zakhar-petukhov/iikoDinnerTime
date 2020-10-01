import json

import pytest
from django.urls import reverse


def get_authorization(api_client, token_user, is_error=False, username='89313147222', password='test'):
    url = reverse('AUTHENTICATION:authentication-login')
    token_user, user = token_user

    data = {
        "username": username,
        "password": password
    }

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    user_data = json.loads(response.content)

    if not is_error:
        assert response.status_code == 200
        assert user_data['first_name'] == 'Тест'

    else:
        assert response.status_code == 400
        assert user_data['non_field_errors'][0] == 'Пользователь с таким юзернеймом и паролем не найден'


@pytest.mark.django_db
class TestAuthenticationView:
    def test_login(self, api_client, token_user):
        get_authorization(api_client, token_user)

    def test_logout(self, api_client, token_user):
        url = reverse('AUTHENTICATION:authentication-logout')
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(url)
        response_logout = json.loads(response.content)

        assert response.status_code == 200
        assert response_logout == 'Успешный выход из системы'

    def test_change_password(self, api_client, token_user):
        url = reverse('AUTHENTICATION:authentication-password-change')
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "current_password": "test",
            "new_password": "TEST",
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 202

    def test_error_change_password(self, api_client, token_user):
        url = reverse('AUTHENTICATION:authentication-password-change')
        token_user, user = token_user
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "current_password": "abrakadabra",
            "new_password": "TEST",
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        response_change_password = json.loads(response.content)

        assert response.status_code == 400
        assert response_change_password['current_password'][0] == 'Текущий пароль не совпадает'

    def test_error_login_username(self, api_client, token_user):
        get_authorization(api_client, token_user, is_error=True, username='hello_people@mail.ru')

    def test_error_login_password(self, api_client, token_user):
        get_authorization(api_client, token_user, is_error=True, password='abrakadabra')
