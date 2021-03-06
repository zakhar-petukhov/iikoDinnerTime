# Generated by Django 2.2.10 on 2020-07-23 18:16

import apps.api.common.models
import apps.api.common.storage
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dinner', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='dish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_dish', to='dinner.Dish', verbose_name='Блюдо'),
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, storage=apps.api.common.storage.OverwriteStorage(), upload_to=apps.api.common.models.Image.get_file_path, verbose_name='Фотография'),
        ),
    ]
