from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import CustomUser
from .models import Project
from .serializers import ProjectSerializer, AddMemberSerializer
from django_filters import rest_framework as django_filters
from django.conf import settings
from django.core.mail import send_mail
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ProjectFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Project
        fields = ['created_after', 'created_before', 'updated_after', 'updated_before']

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj, _):
        return obj.owner == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.OrderingFilter, django_filters.DjangoFilterBackend)
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']
    filterset_class = ProjectFilter

    def get_permissions(self):
        if self.action in ['create', 'list', 'delete', 'add_member', 'remove_member']:
            return [permissions.AllowAny()]
        elif self.action == 'update':
            return [permissions.IsAdminUser(), IsOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.get_user(self.request))

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        elif getattr(settings, 'DEFAULT_ANONYMOUS_USER_DATA', False):
            return self.create_anonymous_user()
        return None

    @action(detail=True, methods=['post'], permission_classes=[IsOwner])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_identifier = request.data.get('user_identifier')

        user = self.get_user_by_identifier(user_identifier)
        if user is None:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        if user in project.members.all():
            return Response({"detail": "Пользователь уже является участником проекта."}, status=status.HTTP_400_BAD_REQUEST)

        project.members.add(user)
        user.current_projects.add(project)
        user.project_history.add(project)

        self.send_notifications(user, project, "Вы добавлены в проект", f"Вы были добавлены в проект: {project.name}")

        return Response({"detail": "Пользователь добавлен в проект."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsOwner])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user_identifier = request.data.get('user_identifier')

        user = self.get_user_by_identifier(user_identifier)
        if user is None:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        if user not in project.members.all():
            return Response({"detail": "Пользователь не является участником проекта."}, status=status.HTTP_400_BAD_REQUEST)

        project.members.remove(user)
        user.current_projects.remove(project)

        self.send_notifications(user, project, "Вы удалены из проекта", f"Вы были удалены из проекта: {project.name}")

        return Response({"detail": "Пользователь удален из проекта."}, status=status.HTTP_200_OK)

    def get_user_by_identifier(self, user_identifier):
        try:
            return CustomUser.objects.get(id=user_identifier)
        except CustomUser.DoesNotExist:
            try:
                return CustomUser.objects.get(username=user_identifier)
            except CustomUser.DoesNotExist:
                return None

    def send_notifications(self, user, project, subject, message):
        self.send_email_notification(user.email, subject, message)
        self.send_websocket_notification(user.id, message)

    def send_email_notification(self, recipient_email, subject, message):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )

    def send_websocket_notification(self, user_id, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {'type': 'send_notification', 'message': message}
        )