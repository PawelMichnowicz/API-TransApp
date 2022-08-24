import zeep
import xmltodict
import json

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from .models import Document
from .serializers import DocumentSerializer
from .constants import WSDL_URL


class DocumentsAPI(mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Document.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = DocumentSerializer


class CheckCompany(APIView):

    permission_classes = [AllowAny, ]

    def get(self, request, format=None):
        client = zeep.Client(wsdl=WSDL_URL)
        key_sid = client.service.Zaloguj('abcde12345abcde12345')

        nip = request.data['NIP']
        with client.settings(extra_http_headers={"sid": key_sid}):
            result = client.service.DaneSzukajPodmioty({'Nip': nip})
            xmlpars = xmltodict.parse(result)

        return Response(xmlpars['root'])


