"""
URL mappings for the storage API
"""
from django.urls import include, path
from rest_framework import routers

from .views import (ApproveDeliveryAction, ActionComplainEmail, ActionCoordinatorApi,
                    ActionDirectorApi, AddActionWindonApi,
                    OverwriteWarehouseActionWindowApi, WarehouseApi, WarehouseStatsApi,
                    WorkersStatsApi, ApproveInProgressAction)

app_name = 'storage'

router = routers.SimpleRouter()
router.register('warehouses', WarehouseApi)
router.register('warehouse-stats', WarehouseStatsApi, basename='warehouse-stats')
router.register('actions-for-coordinator', ActionCoordinatorApi, basename='coordinator-action')
router.register('actions-for-director', ActionDirectorApi, basename='director-action')
router.register('workers-stats', WorkersStatsApi, basename='stats')
router.register('warehouse-add-action-window', AddActionWindonApi, basename='add-action-window')


urlpatterns = [
    path('', include(router.urls)),
    path('warehouse-overwrite-action-window/<int:pk>/',
         OverwriteWarehouseActionWindowApi.as_view(), name='overwrite-action-window'),
    path('action-approve-delivery/<int:pk>/',
         ApproveDeliveryAction.as_view(), name='action-approve-delivery'),
    path('action-approve-inprogress/<int:pk>/',
         ApproveInProgressAction.as_view(), name='action-approve-inprogress'),
    path('action-complain-email/<int:pk>/',
         ActionComplainEmail.as_view(), name='action-complain-email'),
]
