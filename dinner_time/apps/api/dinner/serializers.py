from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.api.common.serializers import SettingsSerializer, ImagesSerializer
from apps.api.company.serializers import CompanyDetailSerializer, CompanyGetSerializer
from apps.api.dinner.models import *
from apps.api.dinner.utils import get_day_menu
from apps.api.users.serializers import UserSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class DishNameCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = CategoryDish
        fields = ['id', 'name']


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish
    """

    id = serializers.IntegerField(read_only=False, required=False)
    added_dish = RecursiveField(many=True, read_only=True)
    image_dish = ImagesSerializer(many=True, read_only=True)
    category_dish = DishNameCategorySerializer(required=False)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'added_dish', 'weight', 'description',
                  'category_dish', 'is_active', 'for_complex', 'image_dish')

    def update(self, instance, validated_data):
        category_dish_validated_data = self.validated_data.get('category_dish')
        if not category_dish_validated_data:
            return super().update(instance, validated_data)

        validated_data['category_dish'] = get_object_or_404(CategoryDish, id=category_dish_validated_data.get("id"))
        return super().update(instance, validated_data)


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


class DinnerDishSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = DinnerDish
        fields = ('id', 'dish', 'count_dish')


class DinnerSerializer(serializers.ModelSerializer):
    """
    Serializer for dinner
    """

    dinner_to_dish = DinnerDishSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    company = CompanyDetailSerializer(required=False)

    class Meta:
        model = Dinner
        fields = ['id', 'dinner_to_dish', 'user', 'company', 'create_date', 'date_action_begin', 'status', 'full_cost',
                  'status_name']

    def create(self, validated_data):
        request = self.context.get('request')
        company_id = request.user.parent if request.user.parent else request.user.id
        user_id = request.user

        data = {
            "user": user_id,
            "company": User.objects.get(id=company_id).company_data
        }

        validated_data.update(data)
        dishes = request.data.pop("dishes", [])
        dinner = Dinner.objects.create(**validated_data)

        for dish in dishes:
            DinnerDish.objects.create(dish_id=dish['id'], dinner=dinner, count_dish=dish['count_dish'])

        return dinner


class DinnerOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for get order dinner
    """

    dinners = DinnerSerializer(many=True)
    company = CompanyGetSerializer(required=False)

    class Meta:
        model = CompanyOrder
        fields = ['id', 'company', 'dinners', 'create_date', 'full_cost', 'send_iiko']

    def validate_dinners(self, value):
        request = self.context.get('request')
        dinners = request.data

        for dinner in dinners['dinners']:
            try:
                dinner = Dinner.objects.get(pk=dinner['id'])
            except ObjectDoesNotExist:
                raise ValidationError("Такого id заказа не существует")

            if dinner.status_name != "Подтвержден":
                raise ValidationError('Статус заказа должен быть "Подтвержден"')

            return dinner

    def create(self, validated_data):
        request = self.context.get('request')
        company = User.objects.get(id=request.user.id, company_data__isnull=False)
        dinners_data = request.data

        company_order = CompanyOrder.objects.create(company=company)

        for dinner in dinners_data['dinners']:
            company_order.dinners.add(dinner["id"])

        return company_order


class WeekMenuSerializer(serializers.ModelSerializer):
    """
    Serializer for week menu
    """

    id = serializers.IntegerField(read_only=False, required=False)
    dishes = MenuSerializer(many=True, required=False)

    class Meta:
        model = WeekMenu
        fields = ['id', 'name', 'number_week', 'dishes']

    def create(self, validated_data):
        dishes = validated_data.get('dishes')

        if not dishes:
            return super().create(validated_data)

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
        if validated_data.get('menu'):
            pk = validated_data.pop('menu')['id']
            week_menu = WeekMenu.objects.get(id=pk)
            return Template.objects.create(menu=week_menu, **validated_data)

        return Template.objects.create(**validated_data)
