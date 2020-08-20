from drf_yasg.openapi import *

request_working_category_dish = Schema(type=TYPE_OBJECT,
                                       properties={
                                           'name': Schema(type=TYPE_STRING, title='Название категории блюда')})

request_for_working_menu = Schema(type=TYPE_OBJECT,
                                  properties={
                                      'dish': Schema(type=TYPE_ARRAY, title='Блюда',
                                                     items=Items(enum={'id': TYPE_INTEGER,
                                                                       'is_remove': TYPE_BOOLEAN}, type=TYPE_STRING)),
                                      'available_order_date': Schema(type=TYPE_STRING,
                                                                     format="date",
                                                                     title='Дата, на которую создано меню'),
                                      'number_day': Schema(type=TYPE_INTEGER)
                                  })

request_for_create_dinner = Schema(type=TYPE_OBJECT,
                                   properties={
                                       'dishes': Schema(type=TYPE_ARRAY, title='Блюда',
                                                        items=Items(enum={'id': TYPE_INTEGER,
                                                                          'count_dish': TYPE_INTEGER},
                                                                    type=TYPE_STRING)),
                                       'date_action_begin': Schema(type=TYPE_STRING, title='Заказ на дату')
                                   })

request_for_week_menu = Schema(type=TYPE_OBJECT,
                               properties={
                                   'name': Schema(type=TYPE_STRING, title='Название шаблона'),
                                   'dishes': Schema(type=TYPE_ARRAY, title='Блюда',
                                                    items=Items(enum={'id': TYPE_INTEGER},
                                                                type=TYPE_STRING)),

                               })

request_for_remove_day_menu_from_week_menu = Schema(type=TYPE_OBJECT,
                                                    properties={
                                                        'dishes': Schema(type=TYPE_ARRAY, title='Блюда',
                                                                         items=Items(enum={'id': TYPE_INTEGER,
                                                                                           'remove': TYPE_BOOLEAN},
                                                                                     type=TYPE_STRING)),

                                                    })
