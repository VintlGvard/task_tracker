import pytest
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task

User = get_user_model()

@pytest.mark.django_db
def test_assign_task_to_user():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user)
    task = Task.objects.create(title='Test Task', description='Task Description', project=project)
    task.assignee = user
    task.save()
    assert task.assignee == user

@pytest.mark.django_db
def test_change_task_assignee():
    user1 = User.objects.create_user(username='user1', password='password1', email='user1@example.com')
    user2 = User.objects.create_user(username='user2', password='password2', email='user2@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user1)
    task = Task.objects.create(title='Test Task', description='Task Description', project=project, assignee=user1)
    task.assignee = user2
    task.save()
    assert task.assignee == user2