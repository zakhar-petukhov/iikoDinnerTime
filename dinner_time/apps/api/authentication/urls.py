from django.urls import path, include
from rest_framework import routers

from api.authentication.views import AuthViewSet

app_name = "AUTHENTICATION"

router = routers.DefaultRouter()
router.register(r'', AuthViewSet, basename='authentication')

urlpatterns = [
    path('', include(router.urls)),
]
