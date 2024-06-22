from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .permissions import IsAdmin
from .serializers import (
    MeSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)
from .utils import create_confirmation_code, send_confirmation_email


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    """Регистрация и получение кода подтверждения."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = create_confirmation_code(user)
        send_confirmation_email(user, confirmation_code)
        return Response({'username': user.username,
                         'email': user.email}, status=status.HTTP_200_OK)


class ObtainTokenView(APIView):
    """Получение JWT токена."""
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Получение всех пользователей или по username."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class MeDetailView(generics.RetrieveUpdateAPIView):
    """Получение данныех своего аккаунта."""
    queryset = User.objects.all()
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
