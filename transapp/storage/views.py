from django.shortcuts import render

from rest_framework import generics, mixins, viewsets

from .models import Warehouse, ReceiveAction , SendAction
from .serializers import WarehouseSerializer, ReceiveActionSerializer, SendActionSerializer
from .serializers import WarehouseDetailSerializer, ReceiveActionDetailSerializer, SendActionDetailSerializer
from core.permissions import IsDirector


class WarehouseApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseDetailSerializer
    permission_classes = [IsDirector,]

    def get_serializer_class(self):
        if self.action == 'list':
            return WarehouseSerializer
        return self.serializer_class


class ReceiveActionApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = ReceiveAction.objects.all()
    serializer_class = ReceiveActionDetailSerializer
    permission_classes = [IsDirector,]

    def get_serializer_class(self):
        if self.action == 'list':
            return ReceiveActionSerializer
        return self.serializer_class


class SendActionApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = SendAction.objects.all()
    serializer_class = SendActionDetailSerializer
    permission_classes = [IsDirector,]

    def get_serializer_class(self):
        if self.action == 'list':
            return SendActionSerializer
        return self.serializer_class