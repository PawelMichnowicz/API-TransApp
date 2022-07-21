from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


from .serializers import VehicleSerializer, RouteSerializer, OfferSerializer, AcceptedOfferSerializer
from .models import Vehicle, Route, Offer, AcceptedOffer
from .permissions import IsDirector

class TestApi(APIView):
    def get(self, request):
        return Response({ "postion":request.user.position})


class VehicleApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsDirector,]


class RouteApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsDirector,]


class OfferApi(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsDirector,]


class AcceptedOfferApi(mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = AcceptedOffer.objects.all()
    serializer_class = AcceptedOfferSerializer
    permission_classes = [IsDirector,]




