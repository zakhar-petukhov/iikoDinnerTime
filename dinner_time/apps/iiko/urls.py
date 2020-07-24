from django.urls import path

from .views import *

urlpatterns = [
    path('create/order/', CreateOrder.as_view(), name="create_order"),

]
