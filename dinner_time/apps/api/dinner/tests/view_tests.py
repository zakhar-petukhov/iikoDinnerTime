import json
from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils.http import urlencode


@pytest.mark.django_db
class TestDinnerView:
    def test_create_category_dish(self, api_client, get_token_company):
        token_company, company = get_token_company
        url = reverse('DINNER:create_dish_category')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Вторые блюда"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        assert user_data['name'] == 'Вторые блюда'

    def test_create_menu(self, api_client, get_token_company, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:create_menu')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dish": [
                {
                    "id": create_dish().id
                }
            ],
            "available_order_date": "2020-05-01"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_get_list_all_category(self, api_client, get_token_company, create_category_dish):
        create_category_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:list_all_category')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data[0]['name'] == 'Первые блюда'

    def test_get_list_category(self, api_client, get_token_company, create_category_dish):
        category = create_category_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:list_category', kwargs={"category_id": category.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data[0]['name'] == 'Первые блюда'

    def test_get_dish(self, api_client, get_token_company, create_complex_dish):
        create_complex_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:list_all_dish')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data[0]['name'] == 'Комплексный обед №1'

    def test_change_dish(self, api_client, get_token_company, create_dish, create_second_category_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_dish', kwargs={"dish_id": create_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Пельмеши",
            "category_dish": {
                "id": create_second_category_dish().id
            },
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)
        assert response.status_code == 200
        assert user_data['category_dish']['name'] == "Вторые блюда"

    def test_change_category_dish(self, api_client, get_token_company, create_category_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_dish_category', kwargs={"dish_category_id": create_category_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Последние блюда"
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)
        assert response.status_code == 200
        assert user_data['name'] == "Последние блюда"

    def test_change_day_menu(self, api_client, get_token_company, create_menu, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_menu', kwargs={"menu_id": create_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dish": [
                {
                    "id": create_dish().id,
                    "is_remove": True
                }
            ],
            "available_order_date": "2020-05-03"
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    def test_delete_dish(self, api_client, get_token_company, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_dish', kwargs={"dish_id": create_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_category_dish(self, api_client, get_token_company, create_category_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_dish_category', kwargs={"dish_category_id": create_category_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_day_menu(self, api_client, get_token_company, create_menu, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_menu', kwargs={"menu_id": create_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_create_week_menu(self, api_client, get_token_company, create_menu):
        token_company, company = get_token_company
        url = reverse('DINNER:week_menu-list')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dishes": [
                {
                    "id": create_menu().id
                }
            ]
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_update_week_menu_add(self, api_client, get_token_company, create_week_menu, create_menu):
        token_company, company = get_token_company
        url = reverse('DINNER:week_menu-detail', kwargs={'pk': create_week_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dishes": [
                {
                    "id": create_menu().id
                }
            ]
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        week_menu_data = json.loads(response.content)

        assert response.status_code == 200
        assert len(week_menu_data['dishes']) == 2

    def test_update_week_menu_remove(self, api_client, get_token_company, create_week_menu, create_menu):
        token_company, company = get_token_company
        url = reverse('DINNER:week_menu-detail', kwargs={'pk': create_week_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dishes": [
                {
                    "id": create_menu().id,
                    "remove": True
                }
            ]
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        week_menu_data = json.loads(response.content)

        assert response.status_code == 200
        assert len(week_menu_data['dishes']) == 1

    def test_delete_week_menu(self, api_client, get_token_company, create_week_menu):
        token_company, company = get_token_company
        url = reverse('DINNER:week_menu-detail', kwargs={'pk': create_week_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.delete(url)

        assert response.status_code == 204

    def test_get_week_menu(self, api_client, get_token_company, create_week_menu):
        token_company, company = get_token_company
        create_week_menu()
        start_menu = datetime.now() - timedelta(days=5)
        close_menu = datetime.now() + timedelta(days=5)
        query_params = {'start_menu': start_menu.strftime("%Y-%m-%d"), 'close_menu': close_menu.strftime("%Y-%m-%d")}

        url = f"{reverse('DINNER:week_menu-list')}?{urlencode(query_params)}"
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        week_menu_data = json.loads(response.content)

        assert response.status_code == 200
        assert len(week_menu_data[0]['dishes']) == 1
