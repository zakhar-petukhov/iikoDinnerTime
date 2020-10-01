from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from apps.api.company.models import Company, DeliveryAddress
from apps.api.users.models import User, Tariff, CustomGroup


class CompanyDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for get all information about company
    """

    class Meta:
        model = Company
        fields = (
            'id', 'company_name', 'city', 'street', 'house', 'house_building', 'apartment', 'legal_address', 'inn',
            'kpp', 'ogrn', 'registration_date', 'bank_name', 'bik', 'corporate_account', 'settlement_account',
            'general_director')


class AddressesSerializer(serializers.ModelSerializer):
    """
    A serializer for company addresses
    """

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'company', 'city', 'street', 'house', 'house_building', 'apartment', 'full_address']

    def create(self, validated_data):
        auth_company = self.context['request'].auth.user.company_data
        instance = DeliveryAddress.objects.create(company=auth_company, **validated_data)

        return instance


class CompanyGetSerializer(serializers.ModelSerializer):
    """
    A serializer for get all company
    """
    from apps.api.users.serializers import UserSerializer, TariffSerializer, GroupSerializer

    all_person = serializers.SerializerMethodField('get_all_person', label='Все сотрудники')
    count_person = serializers.SerializerMethodField('get_count_person', label='Количество сотрудников')
    department = serializers.SerializerMethodField('get_all_department', label='Все отделы')
    all_tariff = serializers.SerializerMethodField('get_all_tariff', label='Все тарифы')
    company_data = CompanyDetailSerializer(required=False)

    def get_count_person(self, obj):
        return User.objects.filter(parent=obj.id).count()

    def get_all_person(self, obj):
        qs = User.objects.filter(parent=obj.id)
        serializer = self.UserSerializer(instance=qs, many=True)
        return serializer.data

    def get_all_department(self, obj):
        qs = CustomGroup.objects.filter(company_id=obj.company_data.id)
        serializer = self.GroupSerializer(instance=qs, many=True)
        return serializer.data

    def get_all_tariff(self, obj):
        qs = Tariff.objects.filter(company_id=obj.company_data.id)
        serializer = self.TariffSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['id', 'company_data', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
                  'count_person', 'all_person', 'department', 'all_tariff', 'is_active']


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for create company
    """

    phone = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    company_data = CompanyDetailSerializer(required=False)

    def validate_phone(self, value):
        phone = PhoneNumber.from_string(phone_number=value, region='RU').as_e164
        return phone

    class Meta:
        model = User
        fields = ['id', 'company_data', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
                  'is_active']
