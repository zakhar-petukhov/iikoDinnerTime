import datetime

from django.db.models import *

from apps.api.users.models import User, CustomGroup


class CompanyOrder(Model):
    company = ForeignKey(User, on_delete=PROTECT, related_name='dinners_orders', blank=True, null=True,
                         verbose_name='Компания')
    dinners = ManyToManyField('dinner.Dinner', related_name='in_orders', blank=True, verbose_name='Заказанные обеды')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    send_iiko = BooleanField(default=False, verbose_name='Отправление в айко')

    @property
    def full_cost(self):
        cost = 0

        all_dinner = self.dinners.all()
        for obj in all_dinner:
            cost += obj.full_cost

        return cost

    @property
    def dinners_oversupply_tariff(self):
        sum_oversupply_tariff = 0

        all_dinner = self.dinners.all()
        for obj in all_dinner:
            sum_oversupply_tariff += obj.oversupply_tariff

        return sum_oversupply_tariff

    class Meta:
        verbose_name = "Одобренное меню"
        verbose_name_plural = "Одобренное меню"


class Dinner(Model):
    IN_PROCESSING = 0
    ACCEPTED = 1
    CANCELED = 2
    CONFIRMED = 3
    STATUSES = [
        (IN_PROCESSING, 'В обработке'),
        (ACCEPTED, 'Принят'),
        (CANCELED, 'Отменен'),
        (CONFIRMED, 'Подтвержден'),
    ]

    dishes = ManyToManyField('dinner.Dish', related_name='dinner_dishes', blank=True, through='dinner.DinnerDish',
                             verbose_name='Блюда')
    user = ForeignKey('users.User', on_delete=PROTECT, related_name='dinner_user', verbose_name='Заказчик',
                      blank=True, null=True)
    company = ForeignKey('company.Company', on_delete=PROTECT, related_name='dinner_company', verbose_name='Компания',
                         blank=True, null=True)

    date_action_begin = DateField(null=True, blank=True, verbose_name='Заказ на дату')
    status = SmallIntegerField(choices=STATUSES, blank=True, default=IN_PROCESSING, verbose_name='Статус')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    update_date = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    @property
    def full_cost(self):
        cost = 0

        all_dinner = self.dishes.all()
        for obj in all_dinner:
            count = obj.dish_to_dinner.get(dish=obj, dinner=self).count_dish
            cost += (obj.cost * count)

        return cost

    @property
    def oversupply_tariff(self):
        if not self.user.company_data:
            tariff = self.user.group.tariff.max_cost_day
            oversupply_cost = tariff - self.full_cost

            if oversupply_cost < 0:
                return abs(oversupply_cost)

        return 0

    @property
    def status_name(self):
        if self.status is not None:
            return self.STATUSES[self.status][1]
        return 'Без статуса'

    class Meta:
        verbose_name = "Обед"
        verbose_name_plural = "Обед"


class CategoryDish(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория блюд"
        verbose_name_plural = "Категория блюд"


class Dish(Model):
    upid = CharField(max_length=43, unique=True, null=True, blank=True, verbose_name='UPID блюда из iiko')
    code = CharField(max_length=43, unique=True, null=True, blank=True, verbose_name='Код блюда из iiko')

    name = CharField(max_length=100, blank=True, null=True, verbose_name='Название блюда')
    added_dish = ManyToManyField('self', related_name='additional_dish', blank=True,
                                 verbose_name='Дополнительное блюдо', symmetrical=False)
    category_dish = ForeignKey(CategoryDish, on_delete=PROTECT, related_name='dishes', verbose_name='Категория блюд',
                               blank=True, null=True)

    cost = FloatField(blank=True, null=True, verbose_name='Цена')
    weight = FloatField(blank=True, null=True, verbose_name='Вес')
    description = CharField(max_length=120, blank=True, null=True, verbose_name='Описание')

    is_active = BooleanField(default=True, verbose_name='Статус активности')
    for_complex = BooleanField(default=False, verbose_name='Для комплексного обеда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюдо"


class DinnerDish(Model):
    dish = ForeignKey(Dish, on_delete=CASCADE, related_name='dish_to_dinner', verbose_name='Блюдо')
    dinner = ForeignKey(Dinner, on_delete=CASCADE, related_name='dinner_to_dish', verbose_name='Обед')
    count_dish = SmallIntegerField(verbose_name='Количество блюд')


class DayMenu(Model):
    dish = ManyToManyField('dinner.Dish', blank=True, verbose_name='Блюда')
    available_order_date = DateField(unique=True, null=True, blank=True, verbose_name='Меню на день')
    number_day = SmallIntegerField(blank=True, null=True, verbose_name='Номер дня недели (если приоритет не дата)')
    close_order_time = ForeignKey('common.Settings', on_delete=PROTECT, null=True, blank=True,
                                  verbose_name='Последний час заказа еды на день')

    # Check whether this menu is available for ordering.
    @property
    def available_for_order(self):
        if self.close_order_time:
            now_time = datetime.datetime.now().strftime('%H.%M')
            if now_time <= self.close_order_time.close_order_time.strftime('%H.%M'):
                return True

    class Meta:
        verbose_name = "Дневное меню"
        verbose_name_plural = "Дневное меню"


class WeekMenu(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название шаблона')
    start_menu = DateField(unique=True, null=True, blank=True, verbose_name='С какого числа показывать меню')
    close_menu = DateField(unique=True, null=True, blank=True, verbose_name='До какого числа действует меню')
    dishes = ManyToManyField('dinner.DayMenu', related_name='week_dishes', blank=True, verbose_name='Дневное меню')

    class Meta:
        verbose_name = "Недельное меню"
        verbose_name_plural = "Недельное меню"
