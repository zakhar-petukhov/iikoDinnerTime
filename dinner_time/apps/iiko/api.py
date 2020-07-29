import json

import requests
from django.conf import settings

from iiko.authentication import get_token


class IikoService:
    def __init__(self):
        self.auth_key = get_token()

    def make_request(self, type, url, payload=None):
        if payload is None:
            payload = {}

        files = {}

        url = settings.IIKO_URL + url

        try:
            response = requests.request(
                method=type, url=url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload),
                files=files, allow_redirects=False, verify=False
            )
        except requests.RequestException:
            raise Exception('Произошла ошибка соединения с сервисом iiko')

        if response.status_code >= 500:
            raise Exception('Произошла ошибка в сервисе iiko')

        response_json = json.loads(response.text)
        return response_json

    def get_organisation(self):
        url = f'organization/list?access_token={self.auth_key}&request_timeout=00:02:00'
        response = self.make_request(type='GET', url=url)
        return response

    def get_nomenclature(self):
        url = f'nomenclature/{settings.IIKO_ORGANIZATION_ID}?organizationId={settings.IIKO_ORGANIZATION_ID}&access_token={self.auth_key}'
        response = self.make_request(type='GET', url=url)
        return response

    def create_company_order(self, data):
        url = f'orders/add?access_token={self.auth_key}&requestTimeout=10000'
        response = self.make_request(type='POST', url=url, payload=data)
        return response
