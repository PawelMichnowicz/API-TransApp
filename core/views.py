from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.authentication import get_authorization_header
from jwt.exceptions import ExpiredSignatureError

from .serializers import UserSerializer
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token


User = get_user_model()

class RegisterApi(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Status": "Założono nowe konto"})
        else:
            return Response({"Status": serializer.errors})


class LoginApi(APIView):
    def post(self, request):
        try:
            user =  User.objects.get(username=request.data['username'])
        except Exception:
            raise APIException('Użytkownik nieaktywny')
        
        if not user.check_password(request.data['password']):
            raise APIException('Nieprawidłowe hasło')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()
        response.set_cookie('refresh_token', refresh_token, httponly=True)
        response.data = {'access_token':access_token}
        return response


class RefreshApi(APIView):
    def post(self,request):
        access_token = request.COOKIES.get('refresh_token')
        return Response({'access_token':access_token})


class TestApi(APIView):
    def get(self, request):
        access_token = get_authorization_header(request).split()[1]
        try:
            user = decode_access_token(access_token)
        except ExpiredSignatureError:
            raise APIException('Refresh your token')
        return Response(user)
