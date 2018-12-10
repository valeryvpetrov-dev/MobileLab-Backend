from rest_framework.generics import GenericAPIView, CreateAPIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate, login, logout

from ..serializers.auth import UserSerializer


class Login(CreateAPIView):
    """
    post:
    Perform login via 'username', 'password' credentials.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({'token': token.key,
                         'user_id': token.user_id},  # !ATTENTION! gets ID from auth_user, not Curator/Student.
                        status=status.HTTP_200_OK)


class Logout(CreateAPIView):
    """
    Methods: POST
    Description: Logout view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)
