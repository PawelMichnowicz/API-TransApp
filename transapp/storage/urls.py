from posixpath import basename
from django.urls import path, include
from rest_framework import routers

from .views import WarehouseApi, ActionCoordinatorApi, WorkersStatsApi, \
    AddActionWindonApi, AcceptAction, AcceptBrokenAction, ActionDirectorApi, \
    WarehouseStatsApi

app_name = 'storage'

router = routers.SimpleRouter()
router.register('warehouses', WarehouseApi)
router.register('warehouse-stats', WarehouseStatsApi,
                basename='warehouse-stats')
router.register('actions-all', ActionCoordinatorApi)
router.register('actions-warehouse', ActionDirectorApi,
                basename='actions-warehouse')
router.register('worker-stats', WorkersStatsApi, basename='stats')
router.register('add-action-window', AddActionWindonApi, basename='add-action-window')


urlpatterns = [
    path('', include(router.urls)),
    path('action-approve/<int:pk>/',
         AcceptAction.as_view(), name='action-approve'),
    path('action-approve-broken/<int:pk>/',
         AcceptBrokenAction.as_view(), name='action-approve-broken'),
]
