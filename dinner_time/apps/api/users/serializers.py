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
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = Tariff
        fields = ['id', 'name', 'company', 'max_cost_day', 'description', 'is_blocked']


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for for working with group
    """

    tariff = TariffSerializer(required=False)

    count_person = serializers.SerializerMethodField('get_count_person', label='Количество сотрудников')

    def get_count_person(self, obj):
        return User.objects.filter(group=obj).count()

    class Meta:
        model = CustomGroup
        fields = ['id', 'tariff', 'name', 'count_person', 'company']

    def create(self, validated_data):
        auth_company = self.context['request'].auth.user.company_data
        user = [self.context['request'].auth.user]

        if not CustomGroup.objects.filter(user_group__in=user).exists():
            tariff, _ = Tariff.objects.get_or_create(company=auth_company, name='Для администраторов', unlimited=True)
            admin_group = CustomGroup.objects.create(name='Администрация', company=auth_company, tariff=tariff)
            admin_group.user_group.set(user)

        instance = CustomGroup.objects.create(company=auth_company, **validated_data)
        return instance


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
