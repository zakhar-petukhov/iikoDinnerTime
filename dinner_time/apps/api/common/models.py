import datetime
import os
import secrets

from config_models.models import ConfigurationModel
from django.conf import settings
from django.db.models import *
from django.utils.safestring import mark_safe
from easy_thumbnails.fields import ThumbnailerImageField

from apps.api.common.storage import OverwriteStorage


class Settings(ConfigurationModel):
    close_order_time = TimeField(default=datetime.time(15, 00), verbose_name='Окончание действия меню')


class ReferralLink(Model):
    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)

    upid = CharField(max_length=43, unique=True, null=True, blank=True, verbose_name='UPID')
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='ref_link', blank=True, null=True,
                      verbose_name='Пользователь')
    is_active = BooleanField(default=True, verbose_name='Активность ссылки')

    def __str__(self):
        return settings.REFERRAL_BASE_URL + f'/{self.pk}/'

    # Genarate UPID
    @classmethod
    def get_generate_upid(self):
        upid = secrets.token_urlsafe()
        return upid

    class Meta:
        verbose_name = 'Реферальная ссылка'


class Image(Model):
    user = ForeignKey('users.User', on_delete=SET_NULL, null=True, blank=True, related_name='image_user',
                      verbose_name='Пользователь')

    dish = ForeignKey('dinner.Dish', on_delete=SET_NULL, null=True, blank=True, related_name='image_dish',
                      verbose_name='Блюдо')

    info = CharField(max_length=20, verbose_name='Описание', blank=True, null=True)
    type = CharField(max_length=6, choices=[
        ('dish', 'Блюдо'),
        ('complex_dinner', 'Комплексный обед'),
        ('avatar', 'Аватар')], verbose_name='Тип фотографии')

    def get_file_path(self, filename):
        ext = filename.split('.')[-1]

        filename_site = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.{ext}"

        if self.type == 'dish':
            return os.path.join(f"{self.type}/{self.dish.id}/images/", filename_site)

        elif self.type == 'avatar':
            return os.path.join(f"{self.type}/{self.user.id}/images/", filename_site)

    image = ThumbnailerImageField(storage=OverwriteStorage(), upload_to=get_file_path, blank=True, null=True,
                                  resize_source=dict(size=(450, 500)), verbose_name='Фотография')

    def img(self):
        if self.image:
            return mark_safe(
                f'<a href="{self.image.url}" target="_blank"><img src="{self.image.url}" width="100"/></a>')
        else:
            return '(Нет изображения)'

    class Meta:
        verbose_name = 'Фотографии'
        verbose_name_plural = 'Фотографии'
