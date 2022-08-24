from suds.xsd.doctor import Import, ImportDoctor
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import logging
logging.basicConfig(level=logging.INFO)


# url = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl'
# client = Client(url)


url = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl?wsdl'
imp = Import("http://CIS/BIR/PUBL/2014/07/DataContract")
imp2 = Import("http://schemas.xmlsoap.org/ws/2005/07/securitypolicy")
doctor = ImportDoctor(imp, imp2)

# client = Client(url, doctor=doctor)
# content = client.factory.create('Content-Type')
# content.set('application/soap+xml')
# client.set_options(soapheaders=(content))
# suds.TypeNotFound: Type not found: 'Content-Type'

client = Client(url, doctor=doctor)
client.set_options(headers={'Content-Type': 'application/soap+xml'})
# print(client)
elo = client.service.Zaloguj(pKluczUzytkownika='abcde12345abcde12345')
print(elo)
