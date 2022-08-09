from multiprocessing.connection import deliver_challenge
from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.response import Response

from core.permissions import IsDirector, IsAdmin, WorkHere, IsCoordinator, WorkHereTimespan
from core.models import WorkPosition

from storage.models import OpenningTime, Warehouse, Action, Timespan
from storage.serializers import ActiopnOrderSerializer, OpenningTimeSerializer, WarehouseSerializer, ActionSerializer, TimespanSerializer
from storage.serializers import WarehouseSerializer, WorkerStatsSerializer, WarehouseStatsSerializer
from storage.constants import StatusChoice


class AddTimespanApi(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = [IsDirector, WorkHereTimespan]
    serializer_class = TimespanSerializer


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
    # def get_queryset(self):
    #     delivered = Action.objects.filter(status=StatusChoice.DELIVERED)
    #     delivered_broken = Action.objects.filter(status=StatusChoice.DELIVERED_BROKEN)
    #     return delivered | delivered_broken


class WarehouseApi(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdmin, ]

    def perform_openning_time(self, instance):
        ''' Helper function to handle nested serializer during update and create'''
        openning_time = self.request.data['openning_time']
        for openning_day in openning_time:
            day_obj = OpenningTime.objects.filter(
                weekday=openning_day['weekday'],
                from_hour=openning_day['from_hour'],
                to_hour=openning_day['to_hour'],
            ).first()
            if not day_obj:
                serializer = OpenningTimeSerializer(data=openning_day)
                serializer.is_valid(raise_exception=True)
                day_obj = serializer.save()
            instance.openning_time.add(day_obj)

    def perform_timespan_available(self, instance):
        ''' Helper function to handle nested serializer during update and create'''
        timespan_available = self.request.data['timespan_available']
        for action_time in timespan_available:
            action_time['warehouse'] = instance.pk
            serializer = TimespanSerializer(data=action_time)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def perform_create(self, serializer):
        ''' Add oppening time and action available data during create instance'''
        instance = serializer.save()
        if 'openning_time' in self.request.data:
            self.perform_openning_time(instance)
        if 'timespan_available' in self.request.data:
            self.perform_timespan_available(instance)
        instance.save()

    def perform_update(self, serializer):
        ''' Add oppening time and action available data during update instance'''
        instance = serializer.save()
        if 'openning_time' in self.request.data:
            instance.openning_time.clear()
            self.perform_openning_time(instance)
        if 'timespan_available' in self.request.data:
            instance.timespan_available.all().delete()
            self.perform_timespan_available(instance)
        instance.save()


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
        serializer = self.get_serializer(queryset, many=True)
        data = {}
        for item in serializer.data:
            status = item.pop('status')
            if status in data:
                data[status].append(item)
            else:
                data[status] = [item]
        return Response(data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActiopnOrderSerializer
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
        buyer_email = instance.transport.orders.values_list().filter(
            buyer_email='miseczkag@gmail.com')
        instance.status = StatusChoice.DELIVERED_BROKEN
        return Response(self.get_serializer(instance=instance).data)
