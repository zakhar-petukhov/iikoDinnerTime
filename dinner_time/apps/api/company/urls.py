from django.urls import path

from apps.api.authentication.views import UserChangeRegAuthDataView
from apps.api.company.views import *

app_name = "COMPANY"

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create_company'),
    path('all/', AllCompaniesView.as_view(), name='all_companies'),
    path('detail/<company_id>/', CompanyDetailView.as_view(), name='detail_company'),
    path('change/detail/<company_id>/', CompanyChangeDetailView.as_view(), name='change_detail_company'),
    path('block/<company_id>/', CompanyChangeDetailView.as_view(), name='block_company'),
    path('delete/<company_id>/', CompanyChangeDetailView.as_view(), name='delete_company'),
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='company_change_auth_ref'),

    path('department/create_department/', DepartmentViewSet.as_view({'post': 'create'}), name='department_create'),
    path('department/list/', DepartmentViewSet.as_view({'get': 'list'}), name='department_list'),
    path('department/detail/<department_id>/', DepartmentViewSet.as_view({'get': 'list'}), name='department_detail'),
    path('department/add_user/', DepartmentCreateUserViewSet.as_view({'post': 'create'}),
         name='department_add_user'),

    path('check/employee_order/', DinnerCheckOrderViewSet.as_view({'get': 'list'}), name='check_employee_order'),
    path('check/order/<user_id>/', DinnerCheckOrderViewSet.as_view({'get': 'list'}),
         name='check_employee_order_user_id'),
    path('employee_order/<pk>/', DinnerCheckOrderViewSet.as_view({'put': 'update'}),
         name='update_employee_order'),

    path('order/', CompanyOrderView.as_view({'post': 'create'}), name='send_employee_order_to_admin'),
    path('history/check/dishes/', CheckDishesView.as_view(), name='company_history_check_dishes/'),
    path('history/order/', CompanyOrderView.as_view({'get': 'list'}), name='company_history_order'),
    path('history/order/detail/<order_id>', CompanyOrderView.as_view({'get': 'list'}),
         name='company_history_order_detail')

]
