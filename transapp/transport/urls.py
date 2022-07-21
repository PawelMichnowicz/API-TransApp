from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register('vehicles', views.VehicleApi)
router.register('routes', views.RouteApi)
router.register('offers', views.OfferApi)
router.register('accepted-offers', views.AcceptedOfferApi)

urlpatterns = [
    path('', include(router.urls)),
    path('check2/', views.TestApi.as_view()),
]


