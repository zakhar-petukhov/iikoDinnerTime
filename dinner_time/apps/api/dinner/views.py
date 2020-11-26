from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.api.dinner.serializers import *
from .data_for_swagger import *


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение блюд.',
    operation_description='''
Метод позволяет:
1) получить все категории меню вместе с блюдами.
2) при передаче "dish_id", получаем только блюда в выбранной категории.
''',
    responses={
        '200': openapi.Response('Успешно', DishSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление данных блюда.',
    operation_description='''
Метод позволяет:
1) добавлять блюда в категорию, путем передачи "id" категории в "category_dish".
2) изменять основную информацию о блюде.
''',
    responses={
        '200': openapi.Response('Успешно', DishSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DishViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DishSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_object(self):
        return get_object_or_404(Dish, id=self.kwargs.get("dish_id"), is_active=True)

    def get_queryset(self):
        dish_id = self.kwargs.get('dish_id')
        if dish_id:
            return Dish.objects.filter(id=dish_id, for_complex=False, is_active=True)

        return Dish.objects.filter(for_complex=False, is_active=True)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение категорий меню вместе с блюдами.',
    operation_description='''
Метод позволяет:
1) получить все категории меню вместе с блюдами.
2) при передаче "category_id", получаем только блюда в выбранной категории.
''',

    responses={
        '200': openapi.Response('Успешно', DishCategorySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление названия категории.',
    request_body=request_working_category_dish,
    responses={
        '200': openapi.Response('Успешно', DishCategorySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание категории.',
    request_body=request_working_category_dish,
    responses={
        '201': openapi.Response('Создано', DishCategorySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DishCategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DishCategorySerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return CategoryDish.objects.filter(id=category_id)

        return CategoryDish.objects.all()

    def get_object(self):
        return get_object_or_404(CategoryDish, id=self.kwargs.get("dish_category_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение информации по дневному меню.',
    responses={
        '200': openapi.Response('Успешно', MenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление данных дневного меню.',
    operation_description='''
Метод позволяет:
1) добавить блюда в меню путем добавления "id" блюда в dish.
2) удалять блюда путем добавления "id" блюда в dish и постановки флага is_remove.
3) менять дату показа этого меню.
''',
    request_body=request_for_working_menu,
    responses={
        '200': openapi.Response('Успешно', MenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание дневного меню.',
    operation_description='''
Метод позволяет:
1) собрать меню из блюд путем добавления "id" блюда в dish.
2) установить дату показа этого меню.
3) number_day - является номером дня недели, где 0 - это воскресенье (нужно для темлейтов)
''',
    request_body=request_for_working_menu,
    responses={
        '201': openapi.Response('Создано', MenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class MenuViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get_queryset(self):
        day_id = self.kwargs.get("day_id")
        category_id = self.kwargs.get("category_id")

        query_params = self.request.query_params
        start_menu = query_params['start_menu']
        close_menu = query_params['close_menu']

        if day_id and category_id:
            category_dish = Dish.objects.filter(category_dish=category_id, is_active=True, for_added_dish=False)
            day_menu = DayMenu.objects.filter(
                number_day=day_id,
                week_dishes__start_menu__gte=start_menu, week_dishes__close_menu__lte=close_menu).prefetch_related(
                Prefetch('dish', queryset=category_dish)
            )

            return day_menu

        elif day_id:
            return DayMenu.objects.filter(number_day=day_id, week_dishes__start_menu__gte=start_menu,
                                          week_dishes__close_menu__lte=close_menu)

        return DayMenu.objects.filter(week_dishes__start_menu__gte=start_menu, week_dishes__close_menu__lte=close_menu)

    def get_object(self):
        return get_object_or_404(DayMenu, id=self.kwargs.get("menu_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр недельного меню.',
    responses={
        '200': openapi.Response('Успешно', WeekMenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление недельного меню.',
    operation_description='''
Метод позволяет:
1) добавить в недельное меню еще один день, путем передачи "id" дневного меню.
2) удалить из недельного меню дневное меню, путем передачи "id" дневного меню с флагом "remove": true.
''',
    request_body=request_for_remove_day_menu_from_week_menu,
    responses={
        '200': openapi.Response('Успешно', WeekMenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Удаление недельного меню.',
    responses={
        '204': 'Удалено',
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание недельного меню.',
    operation_description='''
Передаем в "id" значение из DayMenu.
''',
    request_body=request_for_week_menu,
    responses={
        '201': openapi.Response('Создано', WeekMenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class WeekMenuViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WeekMenuSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        start_menu = query_params['start_menu']
        close_menu = query_params['close_menu']

        return WeekMenu.objects.filter(start_menu__gte=start_menu, close_menu__lte=close_menu)

    def get_object(self):
        return get_object_or_404(WeekMenu, id=self.kwargs.get("pk"))
