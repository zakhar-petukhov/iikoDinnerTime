# Generated by Django 2.2.10 on 2020-09-30 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20201001_0239'),
        ('users', '0003_auto_20201001_0239'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='company_address', to='company.Company', verbose_name='Компания'),
        ),
    ]