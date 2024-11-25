from rest_framework import viewsets
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView as DefaultTokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

DEFAULT_ANONYMOUS_USER_DATA = settings.DEFAULT_ANONYMOUS_USER_DATA

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        return [permissions.AllowAny()] if settings.ALLOW_ANONYMOUS_ACCESS else super().get_permissions()

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [permissions.AllowAny()] if settings.ALLOW_ANONYMOUS_ACCESS else [permissions.IsAuthenticated()]

    def get_object(self):
        if settings.ALLOW_ANONYMOUS_ACCESS and not self.request.user.is_authenticated:
            return None
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        if settings.ALLOW_ANONYMOUS_ACCESS and not request.user.is_authenticated:
            return Response(settings.DEFAULT_ANONYMOUS_USER_DATA, status=status.HTTP_200_OK)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if settings.ALLOW_ANONYMOUS_ACCESS and not request.user.is_authenticated:
            return Response({"detail": "Анонимные пользователи не могут обновлять данные."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if settings.ALLOW_ANONYMOUS_ACCESS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        if settings.ALLOW_ANONYMOUS_ACCESS and not request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return super().post(request, *args, **kwargs)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(DefaultTokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def get_permissions(self):
        if settings.ALLOW_ANONYMOUS_ACCESS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        if settings.ALLOW_ANONYMOUS_ACCESS and not request.user.is_authenticated:
            return Response({"detail": "Анонимные пользователи не могут обновлять токены."}, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)
