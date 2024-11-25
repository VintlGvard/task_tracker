from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('archived', 'Архивирован'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_members', blank=True)
    def __str__(self):
        return self.name