from rest_framework import serializers

from apps.api.common.serializers import SettingsSerializer
from apps.api.company.serializers import CompanyDetailSerializer
from apps.api.dinner.models import *
from apps.api.dinner.utils import get_day_menu
from apps.api.users.serializers import UserSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish
    """

    id = serializers.IntegerField(read_only=False, required=False)
    added_dish = RecursiveField(many=True, read_only=True)
    upid = serializers.ReadOnlyField()
    code = serializers.ReadOnlyField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'upid', 'code', 'cost', 'added_dish', 'weight', 'description',
                  'category_dish', 'is_active', 'for_complex')


class DishCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for category dish
    """

    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = CategoryDish
        fields = ['id', 'name', 'dishes']


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for menu (create, update)
    """

    id = serializers.IntegerField(read_only=False, required=False)
    dish = DishSerializer(many=True, required=False)
    close_order_time = SettingsSerializer(required=False)

    class Meta:
        model = DayMenu
        fields = ['id', 'dish', 'available_order_date', 'close_order_time', 'number_day']

    def create(self, validated_data):
        dish_validated_data = validated_data.pop('dish', [])

        menu = DayMenu.objects.create(**validated_data)
        get_day_menu(menu, dish_validated_data)

        return menu

    def update(self, instance, validated_data):
        dish_validated_data = validated_data.pop('dish')

        instance = super().update(instance, validated_data)
        get_day_menu(instance, dish_validated_data)

        return instance

    def to_internal_value(self, data):
        internal_value = super(MenuSerializer, self).to_internal_value(data)

        dishes = data.get("dish", [])

        internal_value.update({
            "dish": dishes
        })

        return internal_value


class DinnerSerializer(serializers.ModelSerializer):
    """
    Serializer for dinner
    """

    dishes = DishSerializer(many=True)
    user = UserSerializer(required=False)
    company = CompanyDetailSerializer(required=False)

    class Meta:
        model = Dinner
        fields = ['id', 'dishes', 'user', 'company', 'date_action_begin', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        company_id = request.user.parent if request.user.parent else request.user.id
        user_id = request.user

        data = {
            "user": user_id,
            "company": User.objects.get(id=company_id).company_data
        }

        validated_data.update(data)
        dishes = validated_data.pop("dishes", [])
        dinner = Dinner.objects.create(**validated_data)

        for dish in dishes:
            dinner.dishes.add(dish["id"])

        return dinner


class DinnerHistoryOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for get order dinner
    """

    dinners = DinnerSerializer(many=True)

    class Meta:
        model = CompanyOrder
        fields = ['id', 'company', 'dinners', 'create_date']


class WeekMenuSerializer(serializers.ModelSerializer):
    """
    Serializer for week menu
    """

    id = serializers.IntegerField(read_only=False, required=False)
    dishes = MenuSerializer(many=True, required=False)

    class Meta:
        model = WeekMenu
        fields = ['id', 'dishes']

    def create(self, validated_data):
        dishes = validated_data['dishes']

        week_menu = WeekMenu.objects.create()

        for dish in dishes:
            day_menu = DayMenu.objects.get(id=dish.get('id'))
            week_menu.dishes.add(day_menu)

        return week_menu

    def update(self, instance, validated_data):
        dishes = self.initial_data.get('dishes')

        for dish in dishes:
            remove = dish.get('remove')
            day_menu = DayMenu.objects.get(id=dish.get('id'))

            if remove:
                instance.dishes.remove(day_menu)
            else:
                instance.dishes.add(day_menu)

        return instance


class TemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for template
    """

    menu = WeekMenuSerializer(required=False)

    class Meta:
        model = Template
        fields = ['id', 'name', 'number_week', 'menu']

    def create(self, validated_data):
        pk = validated_data.pop('menu')['id']
        week_menu = WeekMenu.objects.get(id=pk)
        return Template.objects.create(menu=week_menu, **validated_data)
