import datetime

from apps.api.dinner.models import Dish, WeekMenu


def get_day_menu(instance, dish_validated_data):
    """
    In this function:
    1) we can remove dish from menu
    2) we can add dish in menu
    """

    for dish in dish_validated_data:
        is_remove = dish.get("is_remove", False)

        dish = Dish.objects.get(pk=dish.get('id'))
        if is_remove:
            instance.dish.remove(dish)
        else:
            instance.dish.add(dish)


def get_number_week():
    day_of_month = datetime.datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1
    return week_number


def get_menu_on_two_weeks():
    number_week = get_number_week()
    return WeekMenu.objects.filter(number_week__in=[number_week, number_week + 1])
