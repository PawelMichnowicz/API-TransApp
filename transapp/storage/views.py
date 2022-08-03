import json
from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsDirector, WorkHere
from core.models import WorkPosition

from .models import Warehouse, Action, Timespan
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


class WorkerDowngradeApi(generics.GenericAPIView):

    queryset = get_user_model().objects.filter(position=WorkPosition.WAREHOUSER.value).all()
    permission_classes = [IsDirector, ]

    def post(self, request, pk, format=None):
        user = self.get_object()
        user.email = None
        user.workplace = None
        user.position = WorkPosition.USER.value
        user.save()
        return Response({'username': user.username, 'position': user.position, 'workplace': user.workplace})


class WorkerUpdateApi(mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(position=WorkPosition.USER.value).all()
    permission_classes = [IsDirector, ]
    serializer_class = WarehouseWorkerSerializer

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.position = WorkPosition.WAREHOUSER.value
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class WorkersStatsApi(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(position=WorkPosition.WAREHOUSER.value).all()
    permission_classes = [IsDirector, ]
    serializer_class = WarehouserStatsSerializer


class WarehouseApi(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['partial_update', 'update']:
            return [IsAuthenticated(), IsDirector(), WorkHere()]
        return super().get_permissions()






    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     raise serializers.ValidationError(serializer.validated_data)
    #     # openning_data = json.loads(request.data['openning_time'])
    #     serializer_opne = OpenningTimeSerializer(data=request.data, partial=True)
    #     serializer_opne.is_valid(raise_exception=True)
    #     return super().update(request, *args, **kwargs)


class ActionApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsDirector, ]
