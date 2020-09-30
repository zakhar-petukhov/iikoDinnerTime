# Generated by Django 2.2.10 on 2020-07-23 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Название группы')),
            ],
            options={
                'verbose_name': 'Категория блюд',
                'verbose_name_plural': 'Категория блюд',
            },
        ),
        migrations.CreateModel(
            name='DayMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_order_date', models.DateField(blank=True, null=True, unique=True, verbose_name='Меню на день')),
                ('number_day', models.SmallIntegerField(blank=True, null=True, verbose_name='Номер дня недели (если приоритет не дата)')),
                ('close_order_time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.Settings', verbose_name='Последний час заказа еды на день')),
            ],
            options={
                'verbose_name': 'Дневное меню',
                'verbose_name_plural': 'Дневное меню',
            },
        ),
        migrations.CreateModel(
            name='WeekMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishes', models.ManyToManyField(blank=True, to='dinner.DayMenu', verbose_name='Дневное меню')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Название шаблона')),
                ('number_week', models.SmallIntegerField(blank=True, null=True, verbose_name='Номер недели')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dinner.WeekMenu', verbose_name='Меню')),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблон',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Название блюда')),
                ('cost', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('description', models.CharField(blank=True, max_length=120, null=True, verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус активности')),
                ('is_complex', models.BooleanField(default=False, verbose_name='Комплексный обед')),
                ('category_dish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dishes', to='dinner.CategoryDish', verbose_name='Категория блюд')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюдо',
            },
        ),
        migrations.CreateModel(
            name='Dinner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_action_begin', models.DateField(blank=True, null=True, verbose_name='Заказ на дату')),
                ('status', models.SmallIntegerField(blank=True, choices=[(0, 'В обработке'), (1, 'Принят'), (2, 'Отменен'), (3, 'Подтвержден')], default=0, verbose_name='Статус')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создано')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dinner_company', to='company.Company', verbose_name='Компания')),
                ('dishes', models.ManyToManyField(blank=True, related_name='dinner_dishes', to='dinner.Dish', verbose_name='Блюдо')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dinner_user', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Обед',
                'verbose_name_plural': 'Обед',
            },
        ),
        migrations.AddField(
            model_name='daymenu',
            name='dish',
            field=models.ManyToManyField(blank=True, to='dinner.Dish', verbose_name='Блюда'),
        ),
        migrations.CreateModel(
            name='CompanyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создано')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dinners_orders', to=settings.AUTH_USER_MODEL, verbose_name='Компания')),
                ('dinners', models.ManyToManyField(blank=True, related_name='in_orders', to='dinner.Dinner', verbose_name='Заказанные обеды')),
            ],
            options={
                'verbose_name': 'Одобренное меню',
                'verbose_name_plural': 'Одобренное меню',
            },
        ),
    ]