'''
Views for the document API
'''
import zeep
import xmltodict

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, mixins, generics

from .models import Document
from .serializers import DocumentSerializer, NipSerializer
from .constants import WSDL_URL, GUS_KEY


class DocumentsAPI(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    ''' View for get list of available document '''
    queryset = Document.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = DocumentSerializer


class CheckCompany(generics.GenericAPIView):
    ''' View for get company information from GUS using NIP '''
    permission_classes = [AllowAny, ]
    serializer_class = NipSerializer

    def get(self, request, format=None):
        ''' Use function "DaneSzukajPodmioty" from SOAP protocol to get data about company'''
        client = zeep.Client(wsdl=WSDL_URL)
        key_sid = client.service.Zaloguj(GUS_KEY)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nip = serializer.validated_data['Nip']
        with client.settings(extra_http_headers={"sid": key_sid}):
            result = client.service.DaneSzukajPodmioty({'Nip': nip})
            xmlpars = xmltodict.parse(result)

        return Response(xmlpars['root'])





