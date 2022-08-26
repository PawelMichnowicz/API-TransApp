'''
Views for the storage API
'''
from rest_framework import mixins, viewsets

from core.permissions import IsDirector

from .models import Route, Transport, Vehicle
from .serializers import (RouteSerializer, TransportSerializer,
                          VehicleSerializer)


class VehicleApi(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    ''' View for get list or retrive vehicle model '''
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsDirector, ]


class RouteApi(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    ''' View for get list or retrive route model '''
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsDirector, ]


class TransportApi(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    ''' View for get list or retrive transport model '''
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [IsDirector,]


