from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.constants import WorkPosition

from transport.models import Route, Vehicle, Transport
from transport.serializers import RouteSerializer, VehicleSerializer, TransportSerializer,\
    RouteSerializer, VehicleSerializer

ROUTE_URL_LIST = reverse('transport:route-list')
VEHICLE_URL = reverse('transport:vehicle-list')
TRANSPORT_URL = reverse('transport:transport-list')


def get_detail_url(model, id):
    return reverse(f'transport:{model.__name__.lower()}-detail', args=[id, ])


class TestModels(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username='user', password='123', position=WorkPosition.USER.value)
        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user)

        self.director = get_user_model().objects.create_user(
            username='dire', password='123', position=WorkPosition.DIRECTOR.value)
        self.director_client = APIClient()
        self.director_client.force_authenticate(self.director)

        self.route = Route.objects.create(
            **{'origin': 'a', 'destination': 'b'})
        self.route2 = Route.objects.create(
            **{'origin': 'b', 'destination': 'a'})
        self.vehicle_ref = Vehicle.objects.create(
            **{'registration': 'RKR 204A', 'capacity': 100, 'is_refrigerate': True})
        self.vehicle = Vehicle.objects.create(
            **{'registration': 'RKR 113C', 'capacity': 200, 'is_refrigerate': False})
        self.transport = Transport.objects.create(
            **{'route': self.route, 'need_refrigerate': True})

    def test_list_routes(self):

        res_dir = self.director_client.get(ROUTE_URL_LIST)
        res_usr = self.user_client.get(ROUTE_URL_LIST)
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_detail_route(self):

        res_dir = self.director_client.get(
            get_detail_url(Route, self.route.pk))
        res_usr = self.user_client.get(get_detail_url(Route, self.route.pk))
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        route = Route.objects.get(pk=self.route.pk)
        serializer = RouteSerializer(route)
        self.assertEqual(res_dir.data, serializer.data)

    def test_list_vehicles(self):

        res_dir = self.director_client.get(VEHICLE_URL)
        res_usr = self.user_client.get(VEHICLE_URL)
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_detail_vehicle(self):

        res_dir = self.director_client.get(
            get_detail_url(Vehicle, self.vehicle.pk))
        res_usr = self.user_client.get(
            get_detail_url(Vehicle, self.vehicle.pk))
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        vehicle = Vehicle.objects.get(registration=self.vehicle.registration)
        serializer = VehicleSerializer(vehicle)
        self.assertEqual(res_dir.data, serializer.data)

    def test_list_transports(self):

        res_dir = self.director_client.get(TRANSPORT_URL)
        res_usr = self.user_client.get(TRANSPORT_URL)
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        transports = Transport.objects.all()
        serializer = TransportSerializer(transports, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_detail_transport(self):

        res_dir = self.director_client.get(
            get_detail_url(Transport, self.transport.pk))
        res_usr = self.user_client.get(
            get_detail_url(Transport, self.transport.pk))
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        transport = Transport.objects.get(pk=self.transport.pk)
        serializer = TransportSerializer(transport)
        self.assertEqual(res_dir.data, serializer.data)
