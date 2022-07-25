from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'storage'

router = routers.SimpleRouter()
router.register('warehouses', views.WarehouseApi)
router.register('receives_action', views.ReceiveActionApi)
router.register('send_actions', views.SendActionApi)


urlpatterns = [
    path('', include(router.urls)),
]


