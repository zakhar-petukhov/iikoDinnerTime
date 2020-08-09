from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from apps.api.common.serializers import ImagesSerializer
from apps.api.users.models import Tariff, CustomGroup

User = get_user_model()


class TariffSerializer(serializers.ModelSerializer):
    """
    Serializer for working with tariff
    """

    class Meta:
        model = Tariff
        fields = ['id', 'name', 'max_cost_day', 'description', 'is_blocked']


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for for working with group
    """

    tariff = TariffSerializer()

    class Meta:
        model = CustomGroup
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for create user
    """
    phone = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    def validate_phone(self, value):
        phone = PhoneNumber.from_string(phone_number=value, region='RU').as_e164
        return phone

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'group', 'phone', 'email', 'department']


class UserSerializer(serializers.ModelSerializer):
    """
    Main user serializer for get information
    """

    group = GroupSerializer(required=False)
    image_user = ImagesSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'department', 'email_verified', 'is_blocked',
                  'block_date', 'company_data', 'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level',
                  'parent', 'group', 'user_permissions', 'image_user']


class EmptySerializer(serializers.Serializer):
    pass
