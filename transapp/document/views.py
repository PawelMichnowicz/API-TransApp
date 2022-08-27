'''
Views for the document API
'''
import zeep
import xmltodict

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, mixins, generics, serializers

from document.models import Document, Contractor
from document.serializers import DocumentSerializer, NipSerializer, ContractorSerializer
from .constants import WSDL_URL, GUS_KEY


class DocumentsAPI(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    ''' View for get list of available document '''
    queryset = Document.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = DocumentSerializer

GUS_FIELDS_MAP = {
    "Regon": "regon",
    "Nip": "nip",
    "StatusNip": "status_nip",
    "Nazwa": "nazwa",
    "Wojewodztwo": "province",
    "Powiat": "district",
    "Gmina": "commune",
    "Miejscowosc": "city",
    "KodPocztowy": "zip_code",
    "Ulica": "street",
    "NrNieruchomosci": "street_number",
    "NrLokalu": "apartment_number",
    "Typ": "type",
    "SilosID": "silos_id",
    "DataZakonczeniaDzialalnosci": "end_date_activity",
    "MiejscowoscPoczty": "city_post"
}

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
        existed_instance = Contractor.objects.filter(nip=nip)
        if existed_instance.exists():
            return Response(ContractorSerializer(instance=existed_instance[0]).data)

        with client.settings(extra_http_headers={"sid": key_sid}):
            xml_data = client.service.DaneSzukajPodmioty({'Nip': nip})
        dict_data = xmltodict.parse(xml_data)['root']['dane']
        if dict_data['ErrorMessageEn']:
            return Response(dict_data['ErrorMessageEn'], status=404)
        data = {GUS_FIELDS_MAP[field]: value for field,value in dict_data.items()}
        serializer = ContractorSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)





