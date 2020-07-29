import datetime

from django.db.models import *

from apps.api.users.models import User


class CompanyOrder(Model):
    company = ForeignKey(User, on_delete=PROTECT, related_name='dinners_orders', blank=True, null=True,
                         verbose_name='Компания')
    dinners = ManyToManyField('dinner.Dinner', related_name='in_orders', blank=True, verbose_name='Заказанные обеды')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')

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

    dishes = ManyToManyField('dinner.Dish', related_name='dinner_dishes', verbose_name='Блюдо', blank=True)
    user = ForeignKey('users.User', on_delete=PROTECT, related_name='dinner_user', verbose_name='Заказчик',
                      blank=True, null=True)
    company = ForeignKey('company.Company', on_delete=PROTECT, related_name='dinner_company', verbose_name='Компания',
                         blank=True, null=True)

    date_action_begin = DateTimeField(null=True, blank=True, verbose_name='Заказ на дату')
    status = SmallIntegerField(choices=STATUSES, blank=True, default=IN_PROCESSING, verbose_name='Статус')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    update_date = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    @property
    def full_cost(self):
        cost = 0
        if not cost:
            all_dinner = self.dishes.all()
            for obj in all_dinner:
                cost += obj.dish.cost

        return cost

    @property
    def status_name(self):
        if self.status:
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


class DayMenu(Model):
    dish = ManyToManyField('dinner.Dish', blank=True, verbose_name='Блюда')
    available_order_date = DateField(unique=True, null=True, blank=True, verbose_name='Меню на день')
    number_day = SmallIntegerField(blank=True, null=True, verbose_name='Номер дня недели (если приоритет не дата)')
    close_order_time = ForeignKey('common.Settings', on_delete=PROTECT, null=True, blank=True,
                                  verbose_name='Последний час заказа еды на день')

    # Check whether this menu is available for ordering.
    @property
    def available_for_order(self):
        now_time = datetime.datetime.now().strftime('%H.%M')
        if now_time <= self.close_order_time.close_order_time.strftime('%H.%M'):
            return True

    class Meta:
        verbose_name = "Дневное меню"
        verbose_name_plural = "Дневное меню"


class WeekMenu(Model):
    dishes = ManyToManyField('dinner.DayMenu', blank=True, verbose_name='Дневное меню')


class Template(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название шаблона')
    number_week = SmallIntegerField(blank=True, null=True, verbose_name='Номер недели')
    menu = ForeignKey('dinner.WeekMenu', on_delete=PROTECT, null=True, blank=True,
                      verbose_name='Меню')

    class Meta:
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблон"
