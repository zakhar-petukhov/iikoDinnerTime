from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from apps.api.company.models import Department, Company
from apps.api.users.models import User, Tariff
from apps.api.users.serializers import UserSerializer, TariffSerializer


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


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for department. Used how main serializer and for create department.
    """

    total_number_users = serializers.SerializerMethodField('get_total_number_users')
    users = serializers.SerializerMethodField('get_users')

    def get_users(self, obj):
        users = UserSerializer(data=User.objects.filter(department=obj.id), many=True)
        users.is_valid()
        return users.data

    def get_total_number_users(self, obj):
        return User.objects.filter(department=obj.id).count()

    class Meta:
        model = Department
        fields = ['id', 'name', 'company', 'total_number_users', 'users']


class CompanyGetSerializer(serializers.ModelSerializer):
    """
    A serializer for get all company
    """

    all_person = serializers.SerializerMethodField('get_all_person', label='Все сотрудники')
    count_person = serializers.SerializerMethodField('get_count_person', label='Количество сотрудников')
    department = serializers.SerializerMethodField('get_all_department', label='Все отделы')
    all_tariff = serializers.SerializerMethodField('get_all_tariff', label='Все тарифы')
    company_data = CompanyDetailSerializer(required=False)

    def get_count_person(self, obj):
        return User.objects.filter(parent=obj.id).count()

    def get_all_person(self, obj):
        qs = User.objects.filter(parent=obj.id)
        serializer = UserSerializer(instance=qs, many=True)
        return serializer.data

    def get_all_department(self, obj):
        qs = Department.objects.filter(company_id=obj.company_data.id)
        serializer = DepartmentSerializer(instance=qs, many=True)
        return serializer.data

    def get_all_tariff(self, obj):
        qs = Tariff.objects.filter(company_id=obj.company_data.id)
        serializer = TariffSerializer(instance=qs, many=True)
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
