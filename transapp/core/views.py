from django.contrib.auth import get_user_model
from django.http import HttpResponse
import jwt

from rest_framework import generics, mixins, viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from storage.serializers import WarehouseWorkerSerializer

from document.models import  Document
from .models import WorkPosition
from .permissions import IsDirector
from .serializers import UserSerializer

from dotenv import dotenv_values

env_var = dotenv_values()
ACCESS_SECRET = env_var['ACCESS_SECRET']
REFRESH_SECRET = env_var['REFRESH_SECRET']
ALG = env_var['ALG']


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
        user.workplace = None
        user.save()
        return Response({'email': user.email, 'position': user.position, 'workplace': user.workplace})


class WorkereCreateApi(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = get_user_model()
    permission_classes = [IsDirector, ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        data = request.data.copy()
        password = get_user_model().objects.make_random_password()
        email = data['email']

        data.update({'email':email, 'password':password, 'password2':password})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        del data['password2']
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)





