from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from api.common.serializers import ImagesSerializer
from api.users.models import Tariff

User = get_user_model()


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'name', 'max_cost_day', 'description', 'is_blocked']


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
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'tariff', 'phone', 'email', 'department']


class UserSerializer(serializers.ModelSerializer):
    """
    Main user serializer for get information
    """

    tariff = TariffSerializer(required=False)
    image_user = ImagesSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'tariff', 'department', 'email_verified', 'is_blocked',
                  'block_date', 'company_data', 'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level',
                  'parent', 'groups', 'user_permissions', 'image_user']


class EmptySerializer(serializers.Serializer):
    pass
