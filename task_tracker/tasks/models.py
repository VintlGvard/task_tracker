from django.db import models
from django.conf import settings
from user.models import CustomUser
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ('Grooming', 'В планах'),
        ('In Progress', 'В работе'),
        ('Dev', 'В разработке'),
        ('Done', 'Выполнен'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Низкий'),
        ('Medium', 'Средний'),
        ('High', 'Высокий'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Grooming')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    tester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_tester', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
