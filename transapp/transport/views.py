from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import VehicleSerializer, RouteSerializer, OfferSerializer
from .serializers import VehicleSerializer, RouteSerializer, OfferSerializer
from .models import Vehicle, Route, Offer
from core.permissions import IsDirector


class TestApi(APIView):
    def get(self, request):
        return Response({"postion": request.user.position})


class VehicleApi(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsDirector, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return VehicleSerializer
        return self.serializer_class


class RouteApi(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsDirector, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteSerializer
        return self.serializer_class


class OfferApi(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsDirector, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferSerializer
        return self.serializer_class
