from posixpath import basename
from django.urls import path, include
from rest_framework import routers

from .views import WarehouseApi, ActionApi, WorkersStatsApi, AddTimespanApi

app_name = 'storage'

router = routers.SimpleRouter()
router.register('warehouses', WarehouseApi)
router.register('actions', ActionApi)
router.register('worker-stats', WorkersStatsApi, basename='stats')



urlpatterns = [
    path('', include(router.urls)),
    path('warehouse-timespan/<int:pk>/',
         AddTimespanApi.as_view(), name='add-timespan'),
]
