from posixpath import basename
from django.urls import path, include
from rest_framework import routers

from .views import WarehouseApi, ActionCoordinatorApi, WorkersStatsApi, \
    AddActionWindonApi, AcceptAction, ActionDirectorApi, \
    WarehouseStatsApi, ActionComplainEmail, OverwriteActionWindowApi

app_name = 'storage'

router = routers.SimpleRouter()
router.register('warehouses', WarehouseApi)
router.register('warehouse-stats', WarehouseStatsApi,
                basename='warehouse-stats')
router.register('actions-for-coordinator', ActionCoordinatorApi)
router.register('actions-for-director', ActionDirectorApi, basename='actions')
router.register('workers-stats', WorkersStatsApi, basename='stats')
router.register('warehouse-add-action-window', AddActionWindonApi, basename='add-action-window')


urlpatterns = [
    path('', include(router.urls)),
    path('warehouse-overwrite-action-window/<int:pk>/',
         OverwriteActionWindowApi.as_view(), name='overwrite-action-window'),
    path('action-approve/<int:pk>/',
         AcceptAction.as_view(), name='action-approve'),
    path('action-complain-email/<int:pk>/',
         ActionComplainEmail.as_view(), name='action-complain-email'),
]
