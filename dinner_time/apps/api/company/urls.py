from django.urls import path

from api.authentication.views import UserChangeRegAuthDataView
from api.company.views import *

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
    path('history/order/', CompanyHistoryOrder.as_view(), name='company_history_order'),
    path('history/order/detail/<order_id>', CompanyHistoryOrder.as_view(), name='company_history_order_detail')

]
