import requests
from django.conf import settings
from django.core.cache import cache


def get_token(refresh=False):
    if not refresh:
        access_token = cache.get('iiko_access_token')

        if access_token:
            return access_token

    login = settings.IIKO_USERNAME
    password = settings.IIKO_PASSWORD
    url = settings.IIKO_AUTHENTIKATION_URL.format(login, password)

    try:
        response = requests.request(method='GET', url=url, headers={'Content-Type': 'application/json'},
                                    allow_redirects=False, verify=False)
    except requests.RequestException:
        raise Exception('Произошла ошибка соединения с сервисом')

    if response.status_code >= 500:
        raise Exception('Произошла ошибка в сервисе iiko')

    access_token = response.text
    cache.set('iiko_access_token', access_token, timeout=45 * 18)

    return access_token
