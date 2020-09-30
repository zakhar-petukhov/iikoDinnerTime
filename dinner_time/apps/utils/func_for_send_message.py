def send_message_for_change_auth_data_company(company_name):
    header = 'Изменения логина и пароля при регистрации компании.'
    body = f'Поздравляем, ваша компания "{company_name}" зарегистрирована на сайте privet-obed.ru!'

    return header, body


def send_message_for_change_auth_data_client(company_name):
    header = 'Изменения логина и пароля при регистрации сотрудника.'
    body = f'Вы добавлены в отдел вашей компании "{company_name}".'

    return header, body


def send_message_for_recovery_password():
    header = 'Изменения пароля.'
    body = 'Для изменения пароля перейдите по ссылки ниже'

    return header, body
