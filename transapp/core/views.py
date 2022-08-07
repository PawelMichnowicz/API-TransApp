from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from storage.serializers import WarehouseWorkerSerializer

from .models import WorkPosition
from .permissions import IsDirector
from .serializers import UserSerializer


class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Status": "Założono nowe konto"})
        else:
            return Response({"Status": serializer.errors})


class WorkerDowngradeApi(generics.GenericAPIView):

    class EmptySerializer(serializers.Serializer):
        pass

    queryset = get_user_model().objects.filter(position=WorkPosition.WAREHOUSER.value).all()
    permission_classes = [IsDirector, ]
    serializer_class = EmptySerializer

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
        return Response({'username': instance.username, 'email':instance.email, 'position': instance.position, 'workplace': instance.workplace.pk})



