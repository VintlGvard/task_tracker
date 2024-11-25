from django.contrib.auth.models import AbstractUser
from django.db import models

from projects.models import Project

ROLE_CHOICES = [
    ('designer', 'Дизайнер'),
    ('analyst', 'Аналитик'),
    ('backend', 'Бекендер'),
    ('tester', 'Тестировщик'),
    ('frontend', 'Фронтендер'),
    ('project_manager', 'Проджект-Менаджер'),
    ('conceptologist', 'Концептолог'),
    ('devops', 'Девопс'),
    ('gd', 'ГД'),
    ('zgd', 'ЗГД'),
]

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    current_projects = models.ManyToManyField(Project, related_name='current_users', blank=True)
    project_history = models.ManyToManyField(Project, related_name='historical_users', blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username