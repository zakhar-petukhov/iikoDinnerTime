from drf_yasg.openapi import *

request_invite_users = Schema(type=TYPE_OBJECT,
                              properties={
                                  'tariff': Schema(type=TYPE_INTEGER, title='ID тарифа'),
                                  'emails': Schema(type=TYPE_ARRAY, title='emails',
                                                   items=Items(enum={'email': TYPE_STRING},
                                                               type=TYPE_STRING))
                              })

request_for_change_user_information = Schema(type=TYPE_OBJECT,
                                             properties={
                                                 'first_name': Schema(type=TYPE_STRING, title='Имя'),
                                                 'last_name': Schema(type=TYPE_STRING, title='Фамилия'),
                                                 'middle_name': Schema(type=TYPE_STRING, title='Отчество'),
                                                 'tariff': Schema(type=TYPE_INTEGER, title='Тариф'),
                                                 'email': Schema(type=TYPE_STRING, title='Email'),
                                                 'department': Schema(type=TYPE_STRING, title='Департамент'),
                                                 'is_blocked': Schema(type=TYPE_BOOLEAN, title='Заблокирован'),
                                             })
