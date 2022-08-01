from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


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

