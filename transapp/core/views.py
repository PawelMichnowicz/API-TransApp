from this import d
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.authentication import get_authorization_header
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
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


        access_token = create_access_token(model_to_dict(user))
        refresh_token = create_refresh_token(user.id)

        response = Response()
        response.set_cookie('refresh_token', refresh_token, httponly=True)
        response.data = {'access_token':access_token}
        return response


class RefreshApi(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)['user_id']
        user = User.objects.get(id=id)
        access_token = create_access_token(model_to_dict(user))
        return Response({'access_token':access_token})


@parser_classes((JSONParser,)) 
class TestApi(APIView):
    def get(self, request):
        token = request.query_params['token']
        user_id = decode_access_token(token)['user_id']
        user = User.objects.get(id=user_id)
        return Response({"username":user.username, "email":user.email})




