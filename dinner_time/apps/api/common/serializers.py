from rest_framework import serializers

from apps.api.common.models import Settings, Image


class SettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for setting. Here is the global settings.
    """

    class Meta:
        model = Settings
        fields = ['id', 'close_order_time', 'enabled']


class ImagesSerializer(serializers.ModelSerializer):
    """
    Serializer for images. Used to add photos to lunches as well as to a user profile.
    """

    class Meta:
        model = Image
        fields = ('id', 'user', 'dish', 'image', 'type')
