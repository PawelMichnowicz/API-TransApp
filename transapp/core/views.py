from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from storage.serializers import WarehouseWorkerSerializer

from .permissions import IsDirector
from .constants import WORK_POSITION
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

    queryset = get_user_model().objects.filter(position=WORK_POSITION[1]).all()
    permission_classes = [IsDirector, ]

    def post(self, request, pk, format=None):
        user = self.get_object()
        user.email = None
        user.workplace = None
        user.position = WORK_POSITION[0]
        user.save()
        return Response({'username': user.username, 'position': user.position, 'workplace': user.workplace})



class WorkerUpdateApi(mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model().objects.filter(position=WORK_POSITION[0]).all()
    permission_classes = [IsDirector, ]
    serializer_class = WarehouseWorkerSerializer

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.position = WORK_POSITION[1]
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
