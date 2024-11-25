from .models import Task, Comment
from django.contrib.auth.models import User
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assignee', 'status', 'priority', 'created_at', 'updated_at', 'due_date', 'tester',]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']