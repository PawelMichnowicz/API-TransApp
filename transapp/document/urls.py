"""
URL mappings for the document API
"""
from django.urls import path, include

from rest_framework import routers

from document.views import  DocumentsAPI, CheckCompany

app_name = 'document'

router = routers.SimpleRouter()
router.register('documents', DocumentsAPI)


urlpatterns = [
    path('', include(router.urls)),
    path('check-company', CheckCompany.as_view())
    ]