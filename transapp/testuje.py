import json
import xmltodict
import zeep


wsdl = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl'
client = zeep.Client(wsdl=wsdl)
# print(dir(client.service))
key_sid = client.service.Zaloguj('abcde12345abcde12345')
print(key_sid)

with client.settings(extra_http_headers={"sid": key_sid}):

    result = client.service.DaneSzukajPodmioty({'Nip': 5250007738})
    xpars = xmltodict.parse(result)

    print(type(xpars))
