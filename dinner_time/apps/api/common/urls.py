from django.urls import path

from api.common.views import SettingsViewSet

app_name = "COMMON"

urlpatterns = [
    path('change_settings/<settings_id>', SettingsViewSet.as_view({'put': 'update'}), name='change_settings'),
    path('list_all_settings/', SettingsViewSet.as_view({'get': 'list'}), name='list_all_settings'),
]
