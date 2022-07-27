from posixpath import basename
from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'storage'

router = routers.SimpleRouter()
router.register('warehouses', views.WarehouseApi)
router.register('receives-action', views.ReceiveActionApi)
router.register('send-actions', views.SendActionApi)
router.register('worker-stats', views.WorkersStatsApi, basename='stats')
router.register('worker-upgrade', views.WorkerUpdateApi, basename='upgrade')


urlpatterns = [
    path('', include(router.urls)),
    path('worker-downgrade/<int:pk>/', views.WorkerDowngradeApi.as_view(), name='downgrade'),
    path('warehouse-timespan/<int:pk>/', views.AddTimespanApi.as_view(), name='add-timespan'),
]
