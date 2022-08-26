"""
URL mappings for the core API
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from document.views import  DocumentsAPI
from .views import RegisterApi, WorkerDowngradeApi,  WorkereCreateApi

app_name = 'core'

router = routers.SimpleRouter()
router.register('documents', DocumentsAPI)
router.register('worker-create', WorkereCreateApi, basename='worker-create')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterApi.as_view()),
    path('token/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('worker-downgrade/<int:pk>/', WorkerDowngradeApi.as_view(), name='downgrade'),
]








