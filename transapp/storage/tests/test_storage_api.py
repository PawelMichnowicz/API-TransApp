from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.test import APIClient

import datetime

from storage.models import Warehouse, Action
from storage.serializers import WarehouserStatsSerializer, ActionSerializer

from core.constants import WORK_POSITION
from storage.constants import TimespanAction

DEFAULT_USER_PARAMS = {
    'username': 'user_',
    'password': '123',
    'position': "USR",
    'workplace': None,
    'email': 'eeelo@wp.pl',
}

def create_worker(**params):

    defaults = DEFAULT_USER_PARAMS.copy()
    defaults.update({'username': 'user_' + get_random_string(length=5)})
    defaults.update(**params)
    return get_user_model().objects.create_user(**defaults)

def create_client(**params):

    user = create_worker(**params)
    user_client = APIClient()
    user_client.force_authenticate(user)
    return user_client


def get_detail_url(model, id):
    return reverse(f'storage:{model.__name__.lower()}-detail', args=[id, ])


class TestPermissionDetailList(TestCase):

    def setUp(self):

        self.user_client = create_client()
        self.dir_client = create_client(**{'position': WORK_POSITION[2]})

        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.send_action = Action.objects.create(
            **{'warehouse': self.warehouse, 'action_type': TimespanAction.SEND})
        self.receive_action = Action.objects.create(
            **{'warehouse': self.warehouse, 'action_type': TimespanAction.RECEIVE})

    def test_list_action(self):

        res_usr = self.user_client.get(reverse('storage:action-list'))
        res_dir = self.dir_client.get(reverse('storage:action-list'))
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)

        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_detail_action(self):

        res_dir = self.dir_client.get(
            get_detail_url(Action, self.send_action.pk))
        res_usr = self.user_client.get(
            get_detail_url(Action, self.send_action.pk))
        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

        send_action = Action.objects.get(pk=self.send_action.pk)
        serializer = ActionSerializer(send_action)
        self.assertEqual(res_dir.data, serializer.data)


class TestModelsMethod(TestCase):

    def setUp(self):

        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.user = create_worker()
        self.worker1 = create_worker(
            **{'position': WORK_POSITION[1], 'workplace': self.warehouse})
        self.worker2 = create_worker(
            **{'position': WORK_POSITION[1], 'workplace': self.warehouse})
        self.receive_action = Action.objects.create(
            **{'warehouse': self.warehouse, 'duration': datetime.timedelta(seconds=(60*60)), 'action_type':TimespanAction.RECEIVE})
        self.send_action = Action.objects.create(
            **{'warehouse': self.warehouse})
        self.receive_action.workers.add(self.worker1)
        self.receive_action.workers.add(self.worker2)
        self.send_action.workers.add(self.worker1)

        self.dir_client = create_client(
            **{'position': WORK_POSITION[2], 'workplace': self.warehouse})
        self.dir_client2 = create_client(**{'position': WORK_POSITION[2], })
        self.user_client = create_client()

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
                    self.assertEqual(
                        sum_time, self.receive_action.duration + self.send_action.duration)
                case self.worker2.username:
                    self.assertEqual(sum_time, self.receive_action.duration)

        workers = get_user_model().objects.filter(position=WORK_POSITION[1]).all()
        serializer = WarehouserStatsSerializer(workers, many=True)
        self.assertEqual(res_dir.data, serializer.data)

        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

    def test_upgrade_worker(self):

        res_usr = self.user_client.patch(reverse('storage:upgrade-detail', args=[self.user.pk]),
                                         {'email': 'example@com.pl', 'workplace': self.warehouse.pk})
        res_dir = self.dir_client.patch(reverse('storage:upgrade-detail', args=[self.user.pk]),
                                        {'email': 'example@com.pl', 'workplace': self.warehouse.pk})
        self.user.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user.email, 'example@com.pl')
        self.assertEqual(self.user.position, WORK_POSITION[1])
        self.assertEqual(
            self.user, self.warehouse.workers.get(id=self.user.pk))

    def test_downgrade_worker(self):

        res_usr = self.user_client.post(
            reverse('storage:downgrade', args=[self.worker1.pk]))
        res_dir = self.dir_client.post(
            reverse('storage:downgrade', args=[self.worker1.pk]))
        self.worker1.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.worker1.email, None)
        self.assertEqual(self.worker1.workplace, None)
        self.assertEqual(self.worker1.position, WORK_POSITION[0])

    def test_add_timespan(self):

        timespan_data = {'monthday': '2022-10-19', 'from_hour': '10:00:00', 'to_hour': '18:00:00', 'action':'send'}
        res_dir = self.dir_client.post(
            reverse('storage:add-timespan', args=[self.warehouse.pk]), timespan_data)
        res_dir2 = self.dir_client2.post(
            reverse('storage:add-timespan', args=[self.warehouse.pk]), timespan_data)

        self.assertEqual(res_dir2.status_code, 403)
        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_dir.data['action_timespan'], timespan_data)
        self.assertEqual(res_dir.data['warehouse_id'], self.warehouse.pk)

