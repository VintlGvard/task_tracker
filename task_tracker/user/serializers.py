from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'role', 'current_projects', 'project_history']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True}}

    def create(self, validated_data):
        if CustomUser.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "Это имя пользователя уже занято."})
        if CustomUser.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Этот адрес электронной почты уже занят."})

        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user