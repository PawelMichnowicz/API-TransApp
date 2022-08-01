from django.urls import path, include
from rest_framework import routers

from .views import VehicleApi, RouteApi, OfferApi

app_name = 'transport'

router = routers.SimpleRouter()
router.register('vehicles', VehicleApi)
router.register('routes', RouteApi)
router.register('offers', OfferApi)

urlpatterns = [
    path('', include(router.urls)),
]




