from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsDirector, IsAdmin, WorkHere
from core.models import WorkPosition

from .models import OpenningTime, Warehouse, Action, Timespan
from .serializers import OpenningTimeSerializer, WarehouseSerializer, ActionSerializer, TimespanSerializer
from .serializers import WarehouseSerializer, WarehouserStatsSerializer, WarehouseWorkerSerializer


class AddTimespanApi(generics.GenericAPIView):

    queryset = Warehouse.objects.all()
    permission_classes = [IsDirector, WorkHere]
    serializer_class = TimespanSerializer

    def post(self, request, pk, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        timespan = serializer.save()

        instance = self.get_object()
        instance.action_available.add(timespan)
        instance.save()

        return Response({'warehouse_id': instance.pk, f'action_timespan': serializer.data})



class WorkersStatsApi(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(position=WorkPosition.WAREHOUSER.value).all()
    permission_classes = [IsDirector, ]
    serializer_class = WarehouserStatsSerializer


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

    def perform_action_available(self, instance):
        ''' Helper function to handle nested serializer during update and create'''
        action_available = self.request.data['action_available']
        for action_time in action_available:
            serializer = TimespanSerializer(data=action_time)
            serializer.is_valid(raise_exception=True)
            action_time_obj = serializer.save()
            instance.action_available.add(action_time_obj)


    def perform_create(self, serializer):
        ''' Add oppening time and action available data during create instance'''
        instance = serializer.save()
        if 'openning_time' in self.request.data:
            self.perform_openning_time(instance)
        if 'action_available' in self.request.data:
            self.perform_action_available(instance)
        instance.save()

    def perform_update(self, serializer):
        ''' Add oppening time and action available data during update instance'''
        instance = serializer.save()
        if self.action =='update':
            instance.action_available.clear()
            instance.openning_time.clear()

        if 'openning_time' in self.request.data:
            self.perform_openning_time(instance)
        if 'action_available' in self.request.data:
            self.perform_action_available(instance)
        instance.save()

class ActionApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsDirector, ]

