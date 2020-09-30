# Generated by Django 2.2.10 on 2020-09-30 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dinner', '0002_dish_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='DinnerDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_dish', models.SmallIntegerField(verbose_name='Количество блюд')),
            ],
        ),
        migrations.AlterModelOptions(
            name='weekmenu',
            options={'verbose_name': 'Недельное меню', 'verbose_name_plural': 'Недельное меню'},
        ),
        migrations.AddField(
            model_name='companyorder',
            name='send_iiko',
            field=models.BooleanField(default=False, verbose_name='Отправление в айко'),
        ),
        migrations.AddField(
            model_name='dish',
            name='added_dish',
            field=models.ManyToManyField(blank=True, related_name='additional_dish', to='dinner.Dish', verbose_name='Дополнительное блюдо'),
        ),
        migrations.AddField(
            model_name='dish',
            name='code',
            field=models.CharField(blank=True, max_length=43, null=True, unique=True, verbose_name='Код блюда из iiko'),
        ),
        migrations.AddField(
            model_name='dish',
            name='for_added_dish',
            field=models.BooleanField(default=False, verbose_name='Добавчное блюдо к главному'),
        ),
        migrations.AddField(
            model_name='dish',
            name='for_complex',
            field=models.BooleanField(default=False, verbose_name='Для комплексного обеда'),
        ),
        migrations.AddField(
            model_name='dish',
            name='upid',
            field=models.CharField(blank=True, max_length=43, null=True, unique=True, verbose_name='UPID блюда из iiko'),
        ),
        migrations.AddField(
            model_name='weekmenu',
            name='close_menu',
            field=models.DateField(blank=True, null=True, unique=True, verbose_name='До какого числа действует меню'),
        ),
        migrations.AddField(
            model_name='weekmenu',
            name='name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Название шаблона'),
        ),
        migrations.AddField(
            model_name='weekmenu',
            name='start_menu',
            field=models.DateField(blank=True, null=True, unique=True, verbose_name='С какого числа показывать меню'),
        ),
        migrations.AlterField(
            model_name='dinner',
            name='dishes',
            field=models.ManyToManyField(blank=True, related_name='dinner_dishes', through='dinner.DinnerDish', to='dinner.Dish', verbose_name='Блюда'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название блюда'),
        ),
        migrations.AlterField(
            model_name='weekmenu',
            name='dishes',
            field=models.ManyToManyField(blank=True, related_name='week_dishes', to='dinner.DayMenu', verbose_name='Дневное меню'),
        ),
        migrations.DeleteModel(
            name='Template',
        ),
        migrations.AddField(
            model_name='dinnerdish',
            name='dinner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinner_to_dish', to='dinner.Dinner', verbose_name='Обед'),
        ),
        migrations.AddField(
            model_name='dinnerdish',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dish_to_dinner', to='dinner.Dish', verbose_name='Блюдо'),
        ),
    ]