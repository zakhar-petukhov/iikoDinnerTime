# Generated by Django 2.2.10 on 2020-10-01 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201001_0239'),
        ('company', '0003_auto_20201001_0239'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address',
            new_name='DeliveryAddress',
        ),
    ]
