from drf_yasg.openapi import *

request_for_dish = Schema(type=TYPE_OBJECT,
                          properties={
                              'name': Schema(type=TYPE_STRING, title='Название блюда'),
                              'cost': Schema(type=TYPE_INTEGER, title='Цена'),
                              'weight': Schema(type=TYPE_INTEGER, title='Вес'),
                              'composition': Schema(type=TYPE_STRING, title='Состав'),
                              'category_dish': Schema(type=TYPE_INTEGER, title='Категория блюд'),
                              'is_active': Schema(type=TYPE_BOOLEAN, title='Активно')
                          })

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
                                                        items=Items(enum={'id': TYPE_INTEGER},
                                                                    type=TYPE_STRING)),
                                       'date_action_begin': Schema(type=TYPE_STRING, title='Заказ на дату')
                                   })

request_for_week_menu = Schema(type=TYPE_OBJECT,
                               properties={
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

request_for_template = Schema(type=TYPE_OBJECT,
                              properties={
                                  'name': Schema(type=TYPE_STRING, title='Название шаблона'),
                                  'number_week': Schema(type=TYPE_INTEGER, title='Номер недели'),
                                  'menu': Schema(type=TYPE_OBJECT, title='Меню',
                                                 properties={
                                                     'id': Schema(type=TYPE_INTEGER, title='id недельного меню')
                                                 })
                              })
