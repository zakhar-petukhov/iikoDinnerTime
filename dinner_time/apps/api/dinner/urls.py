from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.api.common.views import ImageViewSet
from .views import *

app_name = "DINNER"

router = DefaultRouter()
router.register('image', ImageViewSet, base_name='dinner_image')
router.register('template', TemplateViewSet, base_name='template')
router.register('week_menu', WeekMenuViewSet, base_name='week_menu')

urlpatterns = [
    path('create_dish_category/', DishCategoryViewSet.as_view({'post': 'create'}), name='create_dish_category'),
    path('create_menu/', MenuViewSet.as_view({'post': 'create'}), name='create_menu'),

    path('list_menu/<day_id>/', MenuViewSet.as_view({'get': 'list'}), name='list_all_menu'),
    path('list_all_dish/', DishViewSet.as_view({'get': 'list'}), name='list_all_dish'),
    path('dish/<dish_id>/', DishViewSet.as_view({'get': 'list'}), name='list_dish_id'),
    path('list_all_category/', DishCategoryViewSet.as_view({'get': 'list'}), name='list_all_category'),
    path('list_category/<category_id>/', DishCategoryViewSet.as_view({'get': 'list'}), name='list_category'),

    path('change_menu/<menu_id>/', MenuViewSet.as_view({'put': 'update'}), name='change_menu'),
    path('change_dish/<dish_id>/', DishViewSet.as_view({'put': 'update'}), name='change_dish'),
    path('change_dish_category/<dish_category_id>/', DishCategoryViewSet.as_view({'put': 'update'}),
         name='change_dish_category'),

    path('delete_menu/<menu_id>/', MenuViewSet.as_view({'delete': 'destroy'}), name='delete_menu'),
    path('delete_dish/<dish_id>', DishViewSet.as_view({'delete': 'destroy'}), name='delete_dish'),
    path('delete_dish_category/<dish_category_id>', DishCategoryViewSet.as_view({'delete': 'destroy'}),
         name='delete_dish_category'),

    *router.urls
]
