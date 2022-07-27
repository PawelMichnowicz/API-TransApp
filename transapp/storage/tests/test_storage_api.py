from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.test import APIClient

from storage.models import Warehouse, ReceiveAction, SendAction
from storage.serializers import ReceiveActionDetailSerializer, SendActionDetailSerializer, WarehouserStatsSerializer, \
    ReceiveActionSerializer, SendActionSerializer, WarehouseDetailSerializer

import datetime

DEFAULT_USER_PARAMS = {
        'username':'user_',
        'password':'123',
        'position':"USR",
        'workplace':None,
        'email':'eeelo@wp.pl',
    }

def create_worker(**params):

    defaults = DEFAULT_USER_PARAMS.copy()
    defaults.update({'username':'user_'+ get_random_string(length=5)})
    defaults.update(**params)
    return get_user_model().objects.create_user(**defaults)

def create_client(**params):

    user = create_worker(**params)
    user_client = APIClient()
    user_client.force_authenticate(user)
    return user_client




def get_detail_url(model, id):
    return reverse(f'storage:{model.__name__.lower()}-detail', args=[id,])


class TestPermissionDetailList(TestCase):

    def setUp(self):

        self.user_client = create_client()
        self.dir_client = create_client(**{'position':'DIR'})

        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.receive_action = ReceiveAction.objects.create(**{'warehouse': self.warehouse})
        self.send_action = SendAction.objects.create(**{'warehouse': self.warehouse})


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



class TestModelsMethod(TestCase):

    def setUp(self):


        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.worker1 = create_worker(**{'position':'WHR', 'workplace': self.warehouse})
        self.worker2 = create_worker(**{'position':'WHR', 'workplace': self.warehouse})
        self.receive_action = ReceiveAction.objects.create(**{'warehouse': self.warehouse})
        self.receive_action.workers.add(self.worker1)
        self.receive_action.workers.add(self.worker2)
        self.send_action = SendAction.objects.create(**{'warehouse': self.warehouse})
        self.send_action.workers.add(self.worker1)

        self.dir_client = create_client(**{'position':'DIR', 'workplace': self.warehouse})
        self.dir_client2 = create_client(**{'position':'DIR',})
        self.user_client = create_client()
        self.user = create_worker()

    def test_time_worker(self):
        ''' Test user-stats endpoint, calculate sum of hours duration'''
        res_dir = self.dir_client.get(reverse('storage:stats-list'))
        res_usr = self.user_client.get(reverse('storage:stats-list'))

        for user in res_dir.data:
            username = user['username']
            sum_time = datetime.timedelta(seconds=0)
            for stats in user['stats']:
                sum_time += stats['duration']
            match username:
                case self.worker1.username:
                    self.assertEqual(sum_time, self.receive_action.duration + self.send_action.duration)
                case self.worker2.username:
                    self.assertEqual(sum_time, self.receive_action.duration)

        workers = get_user_model().objects.filter(position='WHR').all()
        serializer = WarehouserStatsSerializer(workers, many=True)
        self.assertEqual(res_dir.data, serializer.data)

        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

    def test_upgrade_worker(self):

        res_usr = self.user_client.patch(reverse('storage:upgrade-detail', args=[self.user.pk]),
                                        {'email':'example@com.pl', 'workplace':self.warehouse.pk})
        res_dir = self.dir_client.patch(reverse('storage:upgrade-detail', args=[self.user.pk]),
                                        {'email':'example@com.pl', 'workplace':self.warehouse.pk})
        self.user.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user.email, 'example@com.pl')
        self.assertEqual(self.user.position, 'WHR')
        self.assertEqual(self.user, self.warehouse.workers.get(id=self.user.pk))

    def test_downgrade_worker(self):

        res_usr = self.user_client.post(reverse('storage:downgrade', args=[self.worker1.pk]))
        res_dir = self.dir_client.post(reverse('storage:downgrade', args=[self.worker1.pk]))
        self.worker1.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.worker1.email, None)
        self.assertEqual(self.worker1.workplace, None)
        self.assertEqual(self.worker1.position, 'USR')

    def test_add_timespan(self):

        timespan_data = {'monthday':'2000-01-01',
            'from_hour':'20:00',
            'to_hour':'22:00',
            'action':'send'}
        res_dir = self.dir_client.post(reverse('storage:add-timespan', args=[self.warehouse.pk]), timespan_data)
        res_dir2 = self.dir_client2.post(reverse('storage:add-timespan', args=[self.warehouse.pk]), timespan_data)

        self.assertEqual(res_dir2.status_code, 403)
        self.assertEqual(res_dir.status_code, 200)





