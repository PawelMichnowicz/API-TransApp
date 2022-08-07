from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import VehicleSerializer, RouteSerializer, TransportSerializer
from .serializers import VehicleSerializer, RouteSerializer
from .models import Vehicle, Route, Transport

from core.permissions import IsDirector, IsCoordinator


class TestApi(APIView):
    def get(self, request):
        return Response({"postion": request.user.position})


class VehicleApi(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsDirector, ]


class RouteApi(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsDirector, ]


class TransportApi(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [IsDirector,]



    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return TransportSerializer
    #     return self.serializer_class
