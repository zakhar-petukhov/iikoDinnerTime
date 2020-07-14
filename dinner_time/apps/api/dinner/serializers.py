from rest_framework import serializers

from api.common.serializers import SettingsSerializer
from api.company.serializers import CompanyDetailSerializer
from api.dinner.models import *
from api.dinner.utils import get_additional_dish, get_additional_dish_for_complex, get_day_menu
from api.users.serializers import UserSerializer


class AddedDishSerializer(serializers.ModelSerializer):
    """
    Serializer for add dish to dish
    """

    name = serializers.CharField(source='from_dish.name')
    cost = serializers.FloatField(source='from_dish.cost')
    weight = serializers.FloatField(source='from_dish.weight')
    composition = serializers.CharField(source='from_dish.composition')
    category_dish = serializers.IntegerField(source='from_dish.category_dish.id')

    class Meta:
        model = AddedDish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'category_dish', 'for_complex', 'сomplex_dinner')


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish with create and update method
    """

    id = serializers.IntegerField(read_only=False, required=False)
    added_dish = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'category_dish', 'added_dish', 'is_active')

    def get_added_dish(self, obj):
        is_complex = self.context.get("for_complex", False)
        complex_id = self.context.get("complex_id", None)

        qs = AddedDish.objects.filter(to_dish=obj, for_complex=is_complex, сomplex_dinner=complex_id)
        return [AddedDishSerializer(m).data for m in qs]

    def create(self, validated_data):
        validated_data.pop('added_dish', None)
        create_dish = Dish.objects.create(**validated_data)
        dishes = self.initial_data.get("added_dish", [])
        get_additional_dish(dishes, create_dish)
        return create_dish

    def update(self, instance, validated_data):
        dishes = self.initial_data.get("added_dish", [])
        get_additional_dish(dishes, instance)
        instance.category_dish = validated_data.pop('category_dish', instance.category_dish)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class ComplexDinnerSerializer(serializers.ModelSerializer):
    """
    Serializer for complex dinner with create and update method
    """

    id = serializers.IntegerField(read_only=False, required=False)
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = ComplexDinner
        fields = ['id', 'name', 'dishes']

    def get_dishes(self, obj):
        self.context["complex_id"] = obj.id
        serializer = DishSerializer(many=True, required=False, context=self.context, data=obj.dishes)
        serializer.is_valid()
        return serializer.data

    def create(self, validated_data):
        validated_data.pop("dishes", None)
        complex_dinner = ComplexDinner.objects.create(**validated_data)
        get_additional_dish_for_complex(self.initial_data.get("dishes", []), complex_dinner)
        return complex_dinner

    def update(self, instance, validated_data):
        validated_data.pop("dishes", None)
        get_additional_dish_for_complex(self.initial_data.get("dishes", []), instance)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


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
    complex_dinner = ComplexDinnerSerializer(many=True, required=False)
    close_order_time = SettingsSerializer(required=False)

    class Meta:
        model = DayMenu
        fields = ['id', 'dish', 'complex_dinner', 'available_order_date', 'close_order_time', 'number_day']

    def create(self, validated_data):
        dish_validated_data = validated_data.pop('dish', [])
        complex_dinner_validated_data = validated_data.pop('complex_dinner', [])

        menu = DayMenu.objects.create(**validated_data)
        get_day_menu(menu, dish_validated_data, complex_dinner_validated_data)

        return menu

    def update(self, instance, validated_data):
        dish_validated_data = validated_data.pop('dish')
        complex_dinner_validated_data = validated_data.pop('complex_dinner')

        instance = super().update(instance, validated_data)
        get_day_menu(instance, dish_validated_data, complex_dinner_validated_data)

        return instance

    def to_internal_value(self, data):
        internal_value = super(MenuSerializer, self).to_internal_value(data)

        dishes = data.get("dish", [])
        complex_dinner = data.get("complex_dinner", [])

        internal_value.update({
            "dish": dishes,
            "complex_dinner": complex_dinner
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
