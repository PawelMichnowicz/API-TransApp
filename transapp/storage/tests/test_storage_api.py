from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APIClient


import datetime

from storage.models import Warehouse, Action, ActionChoice
from storage.serializers import WarehouserStatsSerializer, ActionSerializer, WarehouseSerializer

from core.models import WorkPosition


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
        self.dir_client = create_client(**{'position':WorkPosition.DIRECTOR.value})


        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.send_action = Action.objects.create(
            **{'warehouse': self.warehouse, 'action_type': ActionChoice.SEND})
        self.receive_action = Action.objects.create(
            **{'warehouse': self.warehouse, 'action_type': ActionChoice.RECEIVE})

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
        self.warehouse2 = Warehouse.objects.create(**{'name': 'B'})
        self.warehouse3 = Warehouse.objects.create(**{'name': 'C'})
        self.user = create_worker()
        self.worker1 = create_worker(
            **{'position': WorkPosition.WAREHOUSER.value, 'workplace': self.warehouse})
        self.worker2 = create_worker(
            **{'position': WorkPosition.WAREHOUSER.value, 'workplace': self.warehouse})
        self.receive_action = Action.objects.create(
            **{'warehouse': self.warehouse, 'duration': datetime.timedelta(seconds=(60*60)), 'action_type':ActionChoice.RECEIVE})
        self.send_action = Action.objects.create(
            **{'warehouse': self.warehouse})
        self.receive_action.workers.add(self.worker1)
        self.receive_action.workers.add(self.worker2)
        self.send_action.workers.add(self.worker1)

        self.dir_client = create_client(
            **{'position': WorkPosition.DIRECTOR.value, 'workplace': self.warehouse})
        self.dir_client2 = create_client(**{'position': WorkPosition.DIRECTOR.value, })
        self.user_client = create_client()
        self.admin_client = create_client(**{'position':WorkPosition.ADMIN.value})

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

        workers = get_user_model().objects.filter(position=WorkPosition.WAREHOUSER.value).all()
        serializer = WarehouserStatsSerializer(workers, many=True)
        self.assertEqual(res_dir.data, serializer.data)

        self.assertEqual(res_dir.status_code, status.HTTP_200_OK)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)

    def test_upgrade_worker(self):

        res_usr = self.user_client.post(reverse('core:upgrade', args=[self.user.pk]),
                                         {'email': 'example@com.pl', 'workplace': self.warehouse.pk})
        res_dir = self.dir_client.post(reverse('core:upgrade', args=[self.user.pk]),
                                        {'email': 'example@com.pl', 'workplace': self.warehouse.pk})
        self.user.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user.email, 'example@com.pl')
        self.assertEqual(self.user.position, WorkPosition.WAREHOUSER.value)
        self.assertEqual(
            self.user, self.warehouse.workers.get(id=self.user.pk))

    def test_downgrade_worker(self):

        res_usr = self.user_client.post(
            reverse('core:downgrade', args=[self.worker1.pk]))
        res_dir = self.dir_client.post(
            reverse('core:downgrade', args=[self.worker1.pk]))
        self.worker1.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.worker1.email, None)
        self.assertEqual(self.worker1.workplace, None)
        self.assertEqual(self.worker1.position, WorkPosition.USER.value)

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

    def test_CRUD_warehouse(self):

        data = {
            "name": "Updated Name",
            "action_available": [],
            "workers": [],
            "openning_time": [{"weekday": 1, "from_hour": "15:00:00", "to_hour": "18:00:00"}, {"weekday": 2, "from_hour": "15:00:00", "to_hour": "18:00:00"}]
            }

        def updated_data(update_data, data=data):
            new_data = data.copy()
            new_data.update(update_data)
            return new_data

        correct_openning_data = [{"weekday": 1, "from_hour": "10:00:00", "to_hour": "18:00:00"}, {"weekday": 2, "from_hour": "10:00:00", "to_hour": "17:00:00"}]
        wrong_openning_data1 = [{'weekday': 1, 'from_hour': '10:00:00', 'to_hour': '18:00:00'}, {'weekday': 1, 'from_hour': '10:00:00', 'to_hour': '17:00:00'}]
        wrong_openning_data2 = [{'weekday': 1, 'from_hour': '19:00:00', 'to_hour': '18:00:00'}, {'weekday': 2, 'from_hour': '10:00:00', 'to_hour': '17:00:00'}]

        correct_timespan_data = [{"action": "send", "from_hour": "12:22:00", "to_hour": "13:13:00", "monthday": "2022-12-02"},
                                 {"action": "receive", "from_hour": "10:22:00", "to_hour": "13:13:00", "monthday": "2022-12-02"}]
        wrong_timespan_data = [{"action": "send", "from_hour": "12:22:00", "to_hour": "10:13:00", "monthday": "2022-12-02"},
                                 {"action": "receive", "from_hour": "10:22:00", "to_hour": "13:13:00", "monthday": "2022-12-02"}]


        patch_dir = self.dir_client.patch(
            reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
            updated_data({"openning_time":correct_openning_data}),
            format='json')
        patch_admin_wrong = self.admin_client.patch(
            reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
            updated_data({"openning_time":wrong_openning_data1}),
            format='json')
        post_admin_wrong = self.admin_client.post(
            reverse('storage:warehouse-list'),
            updated_data({"openning_time":wrong_openning_data1}),
            format='json')


        put_admin_ok = self.admin_client.put(
            reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
            updated_data({"openning_time":correct_openning_data, 'action_available':correct_timespan_data}),
            format='json')
        patch_admin_ok = self.admin_client.patch(
            reverse('storage:warehouse-detail', args=[self.warehouse2.pk]),
            {"openning_time":correct_openning_data},
            format='json')
        post_admin_ok = self.admin_client.post(
            reverse('storage:warehouse-list'),
            updated_data({"openning_time":correct_openning_data, 'action_available':correct_timespan_data, 'name':'new_name'}),
            format='json')
        delete_admin_ok = self.admin_client.delete(
            reverse('storage:warehouse-detail', args=[self.warehouse3.pk]))


        self.assertEqual(patch_dir.status_code, 403)
        self.assertEqual(patch_admin_wrong.status_code, 400)
        self.assertEqual(post_admin_wrong.status_code, 400)

        try:
            with transaction.atomic():
                self.admin_client.patch(
                    reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
                    updated_data({"openning_time":wrong_openning_data2}),
                    format='json')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                self.admin_client.post(
                    reverse('storage:warehouse-list'),
                    updated_data({"action_available":wrong_timespan_data, 'name':'created_name'}),
                    format='json')
        except IntegrityError:
            pass

        self.warehouse.refresh_from_db()
        self.warehouse2.refresh_from_db()

        self.assertEqual(put_admin_ok.status_code, 200)
        self.assertEqual(patch_admin_ok.status_code, 200)
        self.assertEqual(post_admin_ok.status_code, 201)
        self.assertEqual(delete_admin_ok.status_code, 204)

        self.assertEqual(put_admin_ok.data["name"], self.warehouse.name)
        self.assertEqual(put_admin_ok.data["openning_time"], correct_openning_data)
        self.assertEqual(put_admin_ok.data["action_available"], correct_timespan_data)

        self.assertEqual(patch_admin_ok.data["name"], self.warehouse2.name)
        self.assertEqual(patch_admin_ok.data["openning_time"], correct_openning_data)

        self.assertEqual(post_admin_ok.data["name"], 'new_name')
        self.assertEqual(post_admin_ok.data["openning_time"], correct_openning_data)
        self.assertEqual(post_admin_ok.data["action_available"], correct_timespan_data)

        self.assertFalse(Warehouse.objects.filter(id=self.warehouse3.pk).exists())
