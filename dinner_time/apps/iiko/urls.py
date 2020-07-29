from django.urls import path

from .views import *

urlpatterns = [
    path('create/order/<company_order_id>', CreateOrder.as_view(), name="create_order"),

]
