from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from .serializers import UserSerializer
from .authentication import decode_access_token


User = get_user_model()

class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Status": "Założono nowe konto"})
        else:
            return Response({"Status": serializer.errors})


class TestApi(APIView):
    def get(self, request):
        token = request.query_params['token']
        user_id = decode_access_token(token)['user_id']
        user = User.objects.get(id=user_id)
        return Response({"username":user.username, "email":user.email})