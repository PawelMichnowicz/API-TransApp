import json
import requests

from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.response import Response

from core.permissions import IsDirector, IsAdmin, WorkHere, IsCoordinator, WorkHereActionWindow
from core.models import WorkPosition

from storage.models import OpenningTime, Warehouse, Action, ActionWindow
from storage.serializers import ActionOrderSerializer, OpenningTimeSerializer, WarehouseSerializer, ActionSerializer, ActionWindowSerializer
from storage.serializers import WarehouseSerializer, WorkerStatsSerializer, WarehouseStatsSerializer
from storage.constants import StatusChoice


class WorkersStatsApi(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(
        position=WorkPosition.WAREHOUSER.value).all()
    permission_classes = [IsDirector, ]
    serializer_class = WorkerStatsSerializer


class WarehouseStatsApi(mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [IsCoordinator, WorkHere]
    serializer_class = WarehouseStatsSerializer
    queryset = Warehouse.objects.all()


class WarehouseApi(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdmin, ]

    def include_openning_time(self, instance):
        ''' Helper function to handle nested serializer during update and create'''
        openning_time = self.request.data['openning_time']
        for openning_day in openning_time:
            openning_day['warehouse'] = instance.pk
            serializer = OpenningTimeSerializer(data=openning_day)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def include_action_window(self, instance):
        ''' Helper function to handle nested serializer during update and create'''
        action_window = self.request.data['action_window']
        for action_time in action_window:
            action_time['warehouse'] = instance.pk
            serializer = ActionWindowSerializer(data=action_time)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def perform_create(self, serializer):
        ''' Add oppening time data during create process '''
        instance = serializer.save()
        self.include_openning_time(instance)
        instance.save()

    def perform_update(self, serializer):
        ''' Add oppening time and action available data during update process'''
        instance = serializer.save()
        if 'openning_time' in self.request.data:
            instance.openning_time.all().delete()
            self.include_openning_time(instance)
        if 'action_window' in self.request.data:
            instance.action_window.all().delete()
            self.include_action_window(instance)
        instance.save()


class AddActionWindonApi(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

    permission_classes = [IsDirector, WorkHereActionWindow]
    serializer_class = ActionWindowSerializer


class ActionDirectorApi(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [IsDirector, ]
    serializer_class = ActionSerializer

    def get_queryset(self):
        return Action.objects.filter(warehouse=self.request.user.workplace)


class ActionCoordinatorApi(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsCoordinator, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = {}
        for unique in queryset.values('status').distinct():
            status_queryset = queryset.filter(status=unique['status'])
            serializer = self.get_serializer(status_queryset, many=True)
            data[unique['status']] = serializer.data
        return Response(data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActionOrderSerializer
        return self.serializer_class


class AcceptAction(generics.GenericAPIView):

    queryset = Action.objects.filter(status=StatusChoice.IN_PROGRESS)
    permission_classes = [IsCoordinator]
    serializer_class = ActionSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = StatusChoice.DELIVERED
        instance.save()
        return Response(self.get_serializer(instance=instance).data)


class AcceptBrokenAction(generics.GenericAPIView):

    queryset = Action.objects.filter(status=StatusChoice.IN_PROGRESS)
    permission_classes = [IsCoordinator]
    serializer_class = ActionSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = StatusChoice.DELIVERED_BROKEN
        response = self.get_serializer(instance=instance).data

        data = request.data
        provider = data['provider']
        response['message'] = []
        for order_id in data['broken_orders']:
            email = instance.transport.orders.get(
                order_id=order_id).buyer_email
            send_email_url = f'http://mail:8001/email-complain?provider={provider}'
            send_email_json = {'token': str(request.auth),
                               'email': email,
                               'order_id': order_id,
                               }
            send_email_response = requests.post(
                send_email_url, json=send_email_json)
            if send_email_response.status_code == 200:
                response['message'].append(
                    send_email_response.json()['message'])
            else:
                return Response(send_email_response.json(), status=send_email_response.status_code)

        instance.save()
        return Response(response)
