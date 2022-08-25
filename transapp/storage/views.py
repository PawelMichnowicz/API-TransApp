from binhex import Error
import json
from xml.dom import ValidationErr
import requests

from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Avg, Count
from django.db.models import Q, F
from django.db.utils import IntegrityError

from rest_framework import generics, mixins, viewsets, status, serializers
from rest_framework.response import Response

from core.permissions import IsDirector, IsAdmin, WorkHere, IsCoordinator, WorkHereActionWindow, WorkHereActionObject
from core.models import WorkPosition
from core.functions import send_email

from transport.models import Order

from storage.models import OpenningTime, Warehouse, Action, ActionWindow
from storage.serializers import ActionOrderSerializer, OpenningTimeSerializer, WarehouseSerializer, ActionSerializer, ActionWindowSerializer
from storage.serializers import WarehouseSerializer, WorkerStatsSerializer, ActionWindowOverwriteSerializer, ActionAcceptSerializer
from storage.constants import StatusChoice, BROKEN_ORDER_TEXT, BROKEN_ORDERS_TEXT, SEND_EMAIL_URL
from storage.functions import validate_action_window_date


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
        instance.save()



class OverwriteActionWindowApi(generics.GenericAPIView):

    queryset = Warehouse.objects.all()
    serializer_class = ActionWindowSerializer
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.action_window.all().delete()
        for action_window in request.data['action_windows']:
            action_window['warehouse'] = instance.pk
            serializer = self.get_serializer(data=action_window)
            serializer.is_valid(raise_exception=True)
            validate_action_window_date(serializer, warehouse=instance)
            serializer.save()
        return Response(instance.action_window.values(), status=201)


class AddActionWindonApi(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

    permission_classes = [IsDirector, WorkHereActionWindow]
    serializer_class = ActionWindowSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data['warehouse']
        validate_action_window_date(serializer, warehouse=instance)
        return super().create(request, *args, **kwargs)


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
        queryset = self.get_queryset()
        data = {}
        for unique in queryset.values('status').distinct():
            status_queryset = queryset.filter(Q(status=unique['status']))
            serializer = self.get_serializer(status_queryset, many=True)
            data[unique['status']] = serializer.data
            # qs.annotate(broken=F('pk', filter=Q(pk=1))).values('broken')
        return Response(data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActionOrderSerializer
        return self.serializer_class



class AcceptAction(generics.GenericAPIView):

    queryset = Action.objects.filter(status=StatusChoice.IN_PROGRESS)
    permission_classes = [IsCoordinator, WorkHereActionObject]
    serializer_class = ActionAcceptSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        instance.pk = None

        if not request.data['broken_orders']:
            instance.status = StatusChoice.DELIVERED
        else:
            instance.status = StatusChoice.DELIVERED_BROKEN
            for broken_order in request.data['broken_orders']:
                try:
                    order = instance.transport.orders.get(order_id=broken_order['order_id'])
                except ValidationError as error:
                    raise serializers.ValidationError(error)
                except Order.DoesNotExist as error:
                    raise serializers.ValidationError('order_id_{} {}'.format(broken_order['order_id'], error))
                order.broken = True
                order.save()

        instance.duration = serializer.validated_data['duration']
        try:
            instance.save()
        except IntegrityError as error:
            return Response({'message':f'Action with this id and status is already accepted: {error}'}, status=status.HTTP_409_CONFLICT)
        for worker in serializer.validated_data['workers']:
            instance.workers.add(worker)

        response_api = ActionSerializer(instance=instance).data
        if instance.status == StatusChoice.DELIVERED_BROKEN:
            url = "http://api:8000" + reverse('storage:action-complain-email', args=[instance.pk])
            response_email = requests.post(url=url, data={'provider':'GmailProvider'}, headers={'Authorization': 'Bearer '+str(request.auth)}).text
            response_email = json.loads(response_email)
            response_api.update(response_email)

        return Response(response_api)


class ActionComplainEmail(generics.GenericAPIView):

    queryset = Action.objects.filter(status=StatusChoice.DELIVERED_BROKEN)
    permission_classes = [IsCoordinator]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        api_response = {'email_messages':[], 'email_errors':[]}
        broken_orders = instance.transport.orders.filter(broken=True)
        sorted_orders = broken_orders.values('buyer_email').annotate(list_orders=ArrayAgg('order_id'))
        send_email_url = SEND_EMAIL_URL.format(request.data['provider'])

        for order in sorted_orders:
            if len(order['list_orders'])==1:
                email_text = BROKEN_ORDER_TEXT.format(str(order['list_orders'][0]))
            else:
                email_text = BROKEN_ORDERS_TEXT.format('\n'.join(str(order['list_orders'])))
            email_response = send_email(send_email_url, order['buyer_email'], email_text, token=str(request.auth))
            if email_response.status_code == 200:
                api_response['email_messages'].append(email_response.json())
            else:
                api_response['email_errors'].append(email_response.json())

        return Response(api_response)
