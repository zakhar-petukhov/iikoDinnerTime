from drf_yasg.openapi import *

request_for_update_employee_order = Schema(type=TYPE_OBJECT,
                                           properties={
                                               'date_action_begin': Schema(type=TYPE_STRING, title='Заказ на дату'),
                                               'status': Schema(type=TYPE_INTEGER, title='Статус заказа')
                                           })

request_for_create_order = Schema(type=TYPE_OBJECT,
                                  properties={
                                      'dinners': Schema(type=TYPE_ARRAY, title='Обеды',
                                                        items=Items(enum={'id': TYPE_INTEGER},
                                                                    type=TYPE_STRING)),
                                  })
