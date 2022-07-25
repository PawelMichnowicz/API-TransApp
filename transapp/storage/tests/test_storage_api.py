from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.test import APIClient

from storage.models import Warehouse, ReceiveAction, SendAction
from storage.serializers import ReceiveActionDetailSerializer, SendActionDetailSerializer
from storage.serializers import ReceiveActionSerializer, SendActionSerializer


url = reverse('transport:route-list')

def get_detail_url(model, id):
    return reverse(f'storage:{model.__name__.lower()}-detail', args=[id,])

def create_client(**params):

    defaults = {
        'username':'user_'+ get_random_string(length=5),
        'password':'123',
        'position':"DIR",
        'warehouse':None,
    }
    defaults.update(**params)

    user = get_user_model().objects.create_user(**defaults)
    user_client = APIClient()
    user_client.force_authenticate(user)
    return user_client


class TestStorageModels(TestCase):

    def setUp(self):

        self.dir_client = create_client()
        self.user_client = create_client(**{'position':'USR'})

        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.receive_action = ReceiveAction.objects.create(**{
            'warehouse': self.warehouse,
            })
        self.send_action = SendAction.objects.create(**{
            'warehouse': self.warehouse,
            })


    def test_list_receive_action(self):

        res_usr = self.user_client.get(reverse('storage:receiveaction-list'))
        res_dir = self.dir_client.get(reverse('storage:receiveaction-list'))
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)

        receive_actions = ReceiveAction.objects.all()
        serializer = ReceiveActionSerializer(receive_actions, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_detail_receive_action(self):

        res_dir = self.dir_client.get(get_detail_url(ReceiveAction, self.receive_action.pk))
        res_usr = self.user_client.get(get_detail_url(ReceiveAction, self.receive_action.pk))
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        receive_action = ReceiveAction.objects.get(pk=self.receive_action.pk)
        serializer = ReceiveActionDetailSerializer(receive_action)
        self.assertEqual(res_dir.data, serializer.data)

    def test_list_send_action(self):

        res_usr = self.user_client.get(reverse('storage:sendaction-list'))
        res_dir = self.dir_client.get(reverse('storage:sendaction-list'))
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)

        send_actions = SendAction.objects.all()
        serializer = SendActionSerializer(send_actions, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_detail_send_action(self):

        res_dir = self.dir_client.get(get_detail_url(SendAction, self.send_action.pk))
        res_usr = self.user_client.get(get_detail_url(SendAction, self.send_action.pk))
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        send_action = SendAction.objects.get(pk=self.send_action.pk)
        serializer = SendActionDetailSerializer(send_action)
        self.assertEqual(res_dir.data, serializer.data)