from drf_yasg.openapi import *

request_invite_users = Schema(type=TYPE_OBJECT,
                              properties={
                                  'group': Schema(type=TYPE_INTEGER, title='ID группы'),
                                  'emails': Schema(type=TYPE_ARRAY, title='emails',
                                                   items=Items(enum={'email': TYPE_STRING},
                                                               type=TYPE_STRING))
                              })

request_for_change_user_information = Schema(type=TYPE_OBJECT,
                                             properties={
                                                 'first_name': Schema(type=TYPE_STRING, title='Имя'),
                                                 'last_name': Schema(type=TYPE_STRING, title='Фамилия'),
                                                 'middle_name': Schema(type=TYPE_STRING, title='Отчество'),
                                                 'group': Schema(type=TYPE_INTEGER, title='Группа'),
                                                 'email': Schema(type=TYPE_STRING, title='Email'),
                                                 'department': Schema(type=TYPE_INTEGER, title='Департамент'),
                                                 'is_blocked': Schema(type=TYPE_BOOLEAN, title='Заблокирован'),
                                             })

request_for_create_tariff = Schema(type=TYPE_OBJECT,
                                   properties={
                                       'tariff': Schema(type=TYPE_INTEGER, title='ID тарифа'),
                                       'name': Schema(type=TYPE_STRING, title='Название группы'),
                                   })
