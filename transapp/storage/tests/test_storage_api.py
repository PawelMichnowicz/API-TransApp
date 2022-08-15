from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.test import APIClient

import datetime

from transport.models import Route, Transport

from storage.constants import StatusChoice
from storage.models import ActionChoice
from storage.models import Warehouse, Action, ActionWindow
from storage.serializers import WorkerStatsSerializer, ActionSerializer, WarehouseSerializer, ActionOrderSerializer, ActionWindowSerializer

from core.models import WorkPosition

from collections import OrderedDict


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


class TestStorageApp(TestCase):

    def setUp(self):

        self.route = Route.objects.create()
        self.transport = Transport.objects.create(**{'route': self.route})
        self.transport2 = Transport.objects.create(**{'route': self.route})
        self.transport3 = Transport.objects.create(**{'route': self.route})

        self.initial_name = 'initial B'
        self.warehouse = Warehouse.objects.create(**{'name': 'A'})
        self.warehouse2 = Warehouse.objects.create(
            **{'name': self.initial_name})
        self.warehouse3 = Warehouse.objects.create(**{'name': 'C'})

        self.action_window_send = ActionWindow.objects.create(
            **{'monthday': datetime.datetime(2020, 1, 1),
               'from_hour': datetime.time(12, 00),
               'to_hour': datetime.time(15, 00),
               'action_type': ActionChoice.SEND,
               'warehouse': self.warehouse})
        self.action_window_send2 = ActionWindow.objects.create(
            **{'monthday': datetime.datetime(2020, 1, 2),
               'from_hour': datetime.time(13, 00),
               'to_hour': datetime.time(16, 00),
               'action_type': ActionChoice.SEND,
               'warehouse': self.warehouse})
        self.action_window_receive = ActionWindow.objects.create(
            **{'monthday': datetime.datetime(2020, 1, 3),
               'from_hour': datetime.time(14, 00),
               'to_hour': datetime.time(17, 00),
               'action_type': ActionChoice.RECEIVE,
               'warehouse': self.warehouse})

        self.worker1 = create_worker(
            **{'position': WorkPosition.WAREHOUSER.value,
               'workplace': self.warehouse})
        self.worker2 = create_worker(
            **{'position': WorkPosition.WAREHOUSER.value,
               'workplace': self.warehouse})
        self.user = create_worker()

        self.send_action = Action.objects.create(
            **{'warehouse': self.warehouse,
               'transport': self.transport,
               'action_type': ActionChoice.SEND,
               'status': StatusChoice.DELIVERED,
               'duration': datetime.timedelta(seconds=60*60),
               'action_window': self.action_window_send})
        self.send_action2 = Action.objects.create(
            **{'warehouse': self.warehouse,
               'transport': self.transport2,
               'action_type': ActionChoice.SEND,
               'status': StatusChoice.IN_PROGRESS,
               'duration': datetime.timedelta(seconds=60*60),
               'action_window': self.action_window_send2})
        self.receive_action = Action.objects.create(
            **{'warehouse': self.warehouse,
               'transport': self.transport3,
               'action_type': ActionChoice.RECEIVE,
               'status': StatusChoice.IN_PROGRESS,
               'duration': datetime.timedelta(seconds=2*60*60),
               'action_window': self.action_window_receive})
        self.send_action.workers.add(self.worker1)
        self.receive_action.workers.add(self.worker1)
        self.receive_action.workers.add(self.worker2)

        self.user_client = create_client()
        self.dir_client = create_client(
            **{'position': WorkPosition.DIRECTOR.value,
               'workplace': self.warehouse})
        self.dir_client2 = create_client(
            **{'position': WorkPosition.DIRECTOR.value})
        self.coor_client = create_client(
            **{'position': WorkPosition.COORDINATOR.value})
        self.admin_client = create_client(
            **{'position': WorkPosition.ADMIN.value})

    def test_time_worker(self):
        ''' Test user-stats endpoint, calculate sum of hours duration'''
        res_dir = self.dir_client.get(reverse('storage:stats-list'))
        res_usr = self.user_client.get(reverse('storage:stats-list'))
        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, 403)

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

        workers = get_user_model().objects.filter(
            position=WorkPosition.WAREHOUSER.value).all()
        serializer = WorkerStatsSerializer(workers, many=True)
        self.assertEqual(res_dir.data, serializer.data)

    def test_list_action(self):

        res_usr = self.user_client.get(reverse('storage:action-list'))
        res_dir = self.dir_client.get(reverse('storage:action-list'))
        res_coor = self.coor_client.get(reverse('storage:action-list'))
        self.assertEqual(res_usr.status_code, 403)
        self.assertEqual(res_dir.status_code, 403)
        self.assertEqual(res_coor.status_code, 200)

        delivered_action = ActionSerializer(self.send_action)
        delivered_data = delivered_action.data
        del delivered_data['status']
        delivered_list = [OrderedDict(delivered_data), ]

        inprogress_action = ActionSerializer(self.receive_action)
        inprogress_action2 = ActionSerializer(self.send_action2)
        inprogress_data = inprogress_action.data
        inprogress_data2 = inprogress_action2.data
        del inprogress_data['status']
        del inprogress_data2['status']
        inprogress_list = [
            OrderedDict(inprogress_data2),
            OrderedDict(inprogress_data)]

        self.assertEqual(res_coor.data['delivered'], delivered_list)
        self.assertEqual(res_coor.data['in_progress'], inprogress_list)

    def test_detail_action(self):

        res_dir = self.dir_client.get(
            get_detail_url(Action, self.send_action.pk))
        res_usr = self.user_client.get(
            get_detail_url(Action, self.send_action.pk))
        res_coor = self.coor_client.get(
            get_detail_url(Action, self.send_action.pk))
        self.assertEqual(res_dir.status_code, 403)
        self.assertEqual(res_usr.status_code, 403)
        self.assertEqual(res_coor.status_code, 200)

        send_action = Action.objects.get(pk=self.send_action.pk)
        serializer = ActionOrderSerializer(send_action)
        self.assertEqual(res_coor.data, serializer.data)

    def test_create_worker(self):
        pass

    def test_downgrade_worker(self):

        res_usr = self.user_client.post(
            reverse('core:downgrade', args=[self.worker1.pk]))
        res_dir = self.dir_client.post(
            reverse('core:downgrade', args=[self.worker1.pk]))
        self.worker1.refresh_from_db()

        self.assertEqual(res_dir.status_code, 200)
        self.assertEqual(res_usr.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.worker1.workplace, None)
        # self.assertEqual(self.worker1.position, WorkPosition.USER.value)

    def test_CRUD_warehouse(self):

        data = {
            "name": "Updated Name",
            "action_window": [],
            "workers": [],
            "openning_time": [{"weekday": 1,
                               "from_hour": "15:00:00",
                               "to_hour": "18:00:00"},
                              {"weekday": 2,
                               "from_hour": "15:00:00",
                               "to_hour": "18:00:00"}],
            'action_window': []
        }

        def updated_data(update_data, data=data):
            new_data = data.copy()
            new_data.update(update_data)
            return new_data

        created_name = 'created instance name'
        correct_openning_data = [
            {
                "weekday": 1,
                "from_hour": "10:00:00",
                "to_hour": "18:00:00"},
            {
                "weekday": 2,
                "from_hour": "10:00:00",
                "to_hour": "17:00:00"}
        ]
        wrong_openning_data1 = [{'weekday': 1, 'from_hour': '10:00:00', 'to_hour': '18:00:00'},
                                {'weekday': 1, 'from_hour': '10:00:00', 'to_hour': '17:00:00'}]
        wrong_openning_data2 = [{'weekday': 1, 'from_hour': '19:00:00', 'to_hour': '18:00:00'},
                                {'weekday': 2, 'from_hour': '10:00:00', 'to_hour': '17:00:00'}]

        correct_action_window_data = [
            {"action_type": "send", "from_hour": "12:22:00",
                "to_hour": "13:13:00", "monthday": "2022-12-02"},
            {"action_type": "receive", "from_hour": "10:22:00",
                "to_hour": "13:13:00", "monthday": "2022-12-02"}
        ]
        wrong_action_window_data = [
            {"action_type": "send", "from_hour": "12:22:00",
                "to_hour": "10:13:00", "monthday": "2022-12-02"},
            {"action_type": "receive", "from_hour": "10:22:00",
                "to_hour": "13:13:00", "monthday": "2022-12-02"}
        ]

        patch_dir = self.dir_client.patch(
            reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
            {"openning_time": correct_openning_data},
            format='json')
        patch_admin_wrong = self.admin_client.patch(
            reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
            updated_data({"openning_time": wrong_openning_data1}),
            format='json')
        post_admin_wrong = self.admin_client.post(
            reverse('storage:warehouse-list'),
            updated_data({"openning_time": wrong_openning_data1}),
            format='json')

        put_admin_ok = self.admin_client.put(
            reverse('storage:warehouse-detail', args=[self.warehouse.pk]),
            updated_data({"openning_time": correct_openning_data,
                         'action_window': correct_action_window_data}),
            format='json')
        patch_admin_ok = self.admin_client.patch(
            reverse('storage:warehouse-detail', args=[self.warehouse2.pk]),
            {"openning_time": correct_openning_data},
            format='json')
        post_admin_ok = self.admin_client.post(
            reverse('storage:warehouse-list'),
            updated_data({"openning_time": correct_openning_data,
                         'action_window': correct_action_window_data,
                          'name': created_name}),
            format='json')
        delete_admin_ok = self.admin_client.delete(
            reverse('storage:warehouse-detail', args=[self.warehouse3.pk]))

        # test wrong status code
        self.assertEqual(patch_dir.status_code, 403)
        self.assertEqual(patch_admin_wrong.status_code, 400)
        self.assertEqual(post_admin_wrong.status_code, 400)

        try:
            with transaction.atomic():
                self.admin_client.patch(
                    reverse('storage:warehouse-detail',
                            args=[self.warehouse.pk]),
                    updated_data({"openning_time": wrong_openning_data2}),
                    format='json')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                self.admin_client.post(
                    reverse('storage:warehouse-list'),
                    updated_data(
                        {"action_window": wrong_action_window_data, 'name': created_name}),
                    format='json')
        except IntegrityError:
            pass

        self.warehouse.refresh_from_db()
        self.warehouse2.refresh_from_db()

        # test ok status code
        self.assertEqual(patch_admin_ok.status_code, 200)
        self.assertEqual(put_admin_ok.status_code, 200)
        self.assertEqual(post_admin_ok.status_code, 201)
        self.assertEqual(delete_admin_ok.status_code, 204)

        # put test
        self.assertEqual(data["name"], self.warehouse.name)
        self.assertTrue(self.warehouse.openning_time.filter(
            weekday=correct_openning_data[0]['weekday'],
            from_hour=correct_openning_data[0]['from_hour'],
            to_hour=correct_openning_data[0]['to_hour']
        ).exists())
        self.assertTrue(self.warehouse.openning_time.filter(
            weekday=correct_openning_data[1]['weekday'],
            from_hour=correct_openning_data[1]['from_hour'],
            to_hour=correct_openning_data[1]['to_hour']
        ).exists())
        self.assertEqual(
            len(self.warehouse.openning_time.all()),
            len(correct_openning_data))
        self.assertTrue(self.warehouse.action_window.filter(
            monthday=correct_action_window_data[0]['monthday'],
            from_hour=correct_action_window_data[0]['from_hour'],
            to_hour=correct_action_window_data[0]['to_hour']
        ).exists())
        self.assertTrue(self.warehouse.action_window.filter(
            monthday=correct_action_window_data[1]['monthday'],
            from_hour=correct_action_window_data[1]['from_hour'],
            to_hour=correct_action_window_data[1]['to_hour']
        ).exists())

        self.assertEqual(
            len(self.warehouse.action_window.all()),
            len(correct_action_window_data))

        # patch test
        self.assertEqual(self.initial_name, self.warehouse2.name)
        self.assertTrue(self.warehouse2.openning_time.filter(
            weekday=correct_openning_data[0]['weekday'],
            from_hour=correct_openning_data[0]['from_hour'],
            to_hour=correct_openning_data[0]['to_hour']
        ).exists())
        self.assertTrue(self.warehouse2.openning_time.filter(
            weekday=correct_openning_data[1]['weekday'],
            from_hour=correct_openning_data[1]['from_hour'],
            to_hour=correct_openning_data[1]['to_hour']
        ).exists())
        self.assertEqual(len(self.warehouse.openning_time.all()),
                         len(correct_openning_data))

        # create test
        new_warehouse = Warehouse.objects.get(name=created_name)
        self.assertEqual(created_name, new_warehouse.name)
        self.assertTrue(new_warehouse.openning_time.filter(
            weekday=correct_openning_data[0]['weekday'],
            from_hour=correct_openning_data[0]['from_hour'],
            to_hour=correct_openning_data[0]['to_hour']
        ).exists())
        self.assertTrue(new_warehouse.openning_time.filter(
            weekday=correct_openning_data[1]['weekday'],
            from_hour=correct_openning_data[1]['from_hour'],
            to_hour=correct_openning_data[1]['to_hour']
        ).exists())
        self.assertEqual(
            len(new_warehouse.openning_time.all()),
            len(correct_openning_data))
        self.assertTrue(new_warehouse.action_window.filter(
            monthday=correct_action_window_data[0]['monthday'],
            from_hour=correct_action_window_data[0]['from_hour'],
            to_hour=correct_action_window_data[0]['to_hour']
        ).exists())
        self.assertTrue(new_warehouse.action_window.filter(
            monthday=correct_action_window_data[1]['monthday'],
            from_hour=correct_action_window_data[1]['from_hour'],
            to_hour=correct_action_window_data[1]['to_hour']
        ).exists())
        self.assertEqual(
            len(new_warehouse.action_window.all()),
            len(correct_action_window_data))

        # delete test
        self.assertFalse(Warehouse.objects.filter(
            id=self.warehouse3.pk).exists())

    def test_add_action_window(self):

        action_window_data = {'monthday': '2022-10-19',
                         'from_hour': '10:11:00',
                         'to_hour': '18:13:00',
                         'action_type': 'send',
                         'warehouse': self.warehouse.pk}

        res_dir_workhere = self.dir_client.post(
            reverse('storage:add-action-window-list'),
            action_window_data)
        res_dir_not_workhere = self.dir_client2.post(
            reverse('storage:add-action-window-list'),
            action_window_data)
        self.warehouse.refresh_from_db()

        self.assertEqual(res_dir_not_workhere.status_code, 403)
        self.assertEqual(res_dir_workhere.status_code, 201)

        self.assertTrue(self.warehouse.action_window.filter(
            monthday=action_window_data['monthday'],
            from_hour=action_window_data['from_hour'],
            to_hour=action_window_data['to_hour']
        ).exists())
        self.assertIn(self.action_window_send,
                      self.warehouse.action_window.all())
