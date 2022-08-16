import json
import requests

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.response import Response

from core.permissions import IsDirector, IsAdmin, WorkHere, IsCoordinator, WorkHereActionWindow
from core.models import WorkPosition
from core.functions import send_email

from storage.models import OpenningTime, Warehouse, Action, ActionWindow
from storage.serializers import ActionOrderSerializer, OpenningTimeSerializer, WarehouseSerializer, ActionSerializer, ActionWindowSerializer
from storage.serializers import WarehouseSerializer, WorkerStatsSerializer
from storage.constants import StatusChoice, BROKEN_ORDER_TEXT, BROKEN_ORDERS_TEXT, SEND_EMAIL_URL


class WorkersStatsApi(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(
        position=WorkPosition.WAREHOUSER.value).all()
    permission_classes = [IsDirector, ]
    serializer_class = WorkerStatsSerializer


class WarehouseStatsApi(mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [IsCoordinator, WorkHere]
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        duration = instance.actions.aggregate(Avg('duration'))["duration__avg"]
        total_actions = instance.actions.aggregate(Count('pk'))["pk__count"]
        broken_actions = instance.actions.filter(status=StatusChoice.DELIVERED_BROKEN).aggregate(Count('pk'))["pk__count"]

        return Response({
                    'name_warehouse':instance.name,
                    'avg_duration':duration,
                    'num_total_actions':total_actions,
                    'num_broken_actions':broken_actions
                    })


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

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.pk = None
        match request.data['status']:
            case StatusChoice.DELIVERED.value:
                instance.status = StatusChoice.DELIVERED
            case StatusChoice.DELIVERED_BROKEN.value:
                instance.stats = StatusChoice.DELIVERED_BROKEN
            case _:
                serializers.ValidationError('Invalid status provided')
        instance.save()
        return Response(ActionSerializer(instance=instance).data)



class ActionComplainEmail(generics.GenericAPIView):

    queryset = Action.objects.filter(status=StatusChoice.DELIVERED_BROKEN)
    permission_classes = [IsCoordinator]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        send_email_url = SEND_EMAIL_URL.format(request.data['provider'])
        api_response = {'messages':[]}

        orders = {}
        for order_id in request.data['broken_orders']:
            email = instance.transport.orders.get(order_id=order_id).buyer_email
            if email not in orders:
                orders[email] = [order_id]
            else:
                orders[email].append(order_id)

        for email, orders in orders.items():
            if len(orders)==1:
                email_text = BROKEN_ORDER_TEXT.format(orders[0])
            else:
                email_text = BROKEN_ORDERS_TEXT.format('\n'.join(orders))
            email_response = send_email(send_email_url, email, email_text, token=str(request.auth))
            if email_response.status_code == 200:
                api_response['messages'].append(
                    email_response.json()['message'])
            else:
                return Response(email_response.json(), status=email_response.status_code)

        return Response(api_response)

