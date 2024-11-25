from django_filters.conf import settings
from rest_framework import viewsets, filters, permissions
from django_filters import rest_framework as django_filters
from rest_framework.exceptions import PermissionDenied

from user.models import CustomUser
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer

class TaskFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    updated_at = django_filters.DateFromToRangeFilter()
    due_date = django_filters.DateFromToRangeFilter()
    title = django_filters.CharFilter(lookup_expr='icontains')
    assignee = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)

    class Meta:
        model = Task
        fields = ['status', 'priority', 'assignee', 'created_at', 'updated_at', 'due_date', 'title']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.OrderingFilter, django_filters.DjangoFilterBackend)
    ordering_fields = ['status', 'priority', 'assignee', 'created_at', 'updated_at']
    ordering = ['-created_at']
    filterset_class = TaskFilter

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        elif settings.ALLOW_ANONYMOUS_ACCESS:
            anonymous_user, created = CustomUser.objects.get_or_create(
                username=settings.DEFAULT_ANONYMOUS_USER_DATA['username'],
                defaults=settings.DEFAULT_ANONYMOUS_USER_DATA
            )
            serializer.save(user=anonymous_user)
        else:
            raise PermissionDenied("Анонимный доступ запрещен.")

