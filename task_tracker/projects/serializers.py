from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'status', 'owner', 'members']

class AddMemberSerializer(serializers.Serializer):
    user_identifier = serializers.CharField(required=True, help_text="Логин или ID пользователя")