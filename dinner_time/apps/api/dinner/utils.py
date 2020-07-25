from apps.api.dinner.models import Dish


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
