def send_message_for_change_auth_data_company(url, company_name):
    header = '''Изменения логина и пароля при регистрации компании.'''

    body = f'''
Здравствуйте!

Поздравляем, ваша компания "{company_name}" зарегистрирована на сайте privet-obed.ru!

Вам установлен базовый логин и пароль, для смены, пожалуйста, перейдите по ссылки ниже.

{url}

С уважением, команда privet-obed.ru!
'''
    return header, body


def send_message_for_change_auth_data_client(url, company_name):
    header = '''Изменения логина и пароля при регистрации сотрудника.'''

    body = f'''
Здравствуйте!

Вы добавлены в отдел вашей компании "{company_name}".

Вам установлен базовый логин и пароль, для смены, пожалуйста, перейдите по ссылки ниже.

{url}

С уважением, команда privet-obed.ru!
'''

    return header, body
