from django.urls import path
from rest_framework import routers

from apps.api.authentication.views import UserChangeRegAuthDataView
from apps.api.common.views import ImageViewSet
from apps.api.users.views import *

app_name = "USERS"

router = routers.DefaultRouter()
router.register(r'image', ImageViewSet, base_name='user_image')
router.register(r'group', GroupView, base_name='user_group')
router.register(r'tariff', TariffView, base_name='group_tariff')

urlpatterns = [
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='user_change_auth_ref'),

    path('user/<pk>/detail_information/', UserView.as_view({'get': 'list'}), name='detail_information'),
    path('user/<pk>/', UserView.as_view({'put': 'update'}), name='change_detail_information'),

    path('create/dinner/', UserCreateDinnerView.as_view({'post': 'create'}), name='user_add_dish'),

    path('invite/users/', InviteUsersView.as_view(), name='invite_user'),

    *router.urls
]
