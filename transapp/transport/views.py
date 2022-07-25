from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


from .serializers import VehicleSerializer, RouteSerializer, OfferSerializer, AcceptedOfferSerializer
from .serializers import VehicleDetailSerializer, RouteDetailSerializer, OfferDetailSerializer, AcceptedOfferDetailSerializer
from .models import Vehicle, Route, Offer, AcceptedOffer
from core.permissions import IsDirector

class TestApi(APIView):
    def get(self, request):
        return Response({ "postion":request.user.position})


class VehicleApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailSerializer
    permission_classes = [IsDirector,]

    def get_serializer_class(self):
        if self.action == 'list':
            return VehicleSerializer
        return self.serializer_class

class RouteApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Route.objects.all()
    serializer_class = RouteDetailSerializer
    permission_classes = [IsDirector,]

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteSerializer
        return self.serializer_class


class OfferApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsDirector,]

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferSerializer
        return self.serializer_class


class AcceptedOfferApi(mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = AcceptedOffer.objects.all()
    serializer_class = AcceptedOfferSerializer
    permission_classes = [IsDirector,]




