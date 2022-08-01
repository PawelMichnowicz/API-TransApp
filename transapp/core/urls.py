from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


from .views import RegisterApi, WorkerDowngradeApi
from storage.views import WorkerUpdateApi

app_name = 'core'

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('token/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('worker-downgrade/<int:pk>/', WorkerDowngradeApi.as_view(), name='downgrade'),
    path('worker-upgrade/<int:pk>/', WorkerUpdateApi.as_view({'post': 'update',}), name='upgrade'),
]



