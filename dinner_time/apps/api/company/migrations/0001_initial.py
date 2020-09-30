# Generated by Django 2.2.10 on 2020-07-23 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Название компании')),
                ('full_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Полный адрес')),
                ('legal_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Юридический адрес')),
                ('general_director', models.CharField(blank=True, max_length=45, null=True, verbose_name='Генеральный директор')),
                ('inn', models.CharField(blank=True, max_length=12, null=True, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, max_length=9, null=True, verbose_name='КПП')),
                ('ogrn', models.CharField(blank=True, max_length=9, null=True, verbose_name='ОГРН')),
                ('registration_date', models.DateField(blank=True, null=True, verbose_name='Дата регистрации')),
                ('bank_name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Название банка')),
                ('bik', models.CharField(blank=True, max_length=9, null=True, verbose_name='БИК')),
                ('corporate_account', models.CharField(blank=True, max_length=20, null=True, verbose_name='Корпоративный счет')),
                ('settlement_account', models.CharField(blank=True, max_length=20, null=True, verbose_name='Расчетный счет')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компания',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Название')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='company_department', to='company.Company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департамент',
            },
        ),
    ]