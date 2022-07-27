from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from core.permissions import IsDirector, WorkHere

from .models import Warehouse, Action, Timespan
from .serializers import WarehouseSerializer, ActionSerializer, TimespanSerializer
from .serializers import WarehouseDetailSerializer, WarehouserStatsSerializer, WarehouseWorkerSerializer


class AddTimespanApi(generics.GenericAPIView):

    queryset = Warehouse.objects.all()
    permission_classes = [IsDirector, WorkHere]
    serializer_class = TimespanSerializer

    def post(self, request, pk, *args, **kwargs):

        data = request.data.copy()
        action = str(data.pop('action')[0])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        timespan = serializer.save()

        instance = self.get_object()
        instance.action_available.add(timespan)
        instance.save()

        return Response({'name': 'instance.name', f'{action}_timespan': serializer.data})


class WorkerDowngradeApi(generics.GenericAPIView):

    queryset = get_user_model().objects.filter(position='WHR').all()
    permission_classes = [IsDirector, ]

    def post(self, request, pk, format=None):
        user = self.get_object()
        user.email = None
        user.workplace = None
        user.position = 'USR'
        user.save()
        return Response({'username': user.username, 'position': user.position, 'workplace': user.workplace})


class WorkerUpdateApi(mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(position='USR').all()
    permission_classes = [IsDirector, ]
    serializer_class = WarehouseWorkerSerializer

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.position = 'WHR'
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class WorkersStatsApi(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(position='WHR').all()
    permission_classes = [IsDirector, ]
    serializer_class = WarehouserStatsSerializer


class WarehouseApi(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseDetailSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['partial_update', 'update']:
            return [IsAuthenticated(), IsDirector(), WorkHere()]
        return super().get_permissions()


class ActionApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsDirector, ]

