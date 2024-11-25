import pytest
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task, Comment

User = get_user_model()

@pytest.mark.django_db
def test_project_creation():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user)
    assert project.name == 'Test Project'
    assert project.description == 'Project Description'
    assert project.owner == user
    assert project.status == 'active'

@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user)
    task = Task.objects.create(title='Test Task', description='Task Description', project=project, assignee=user)
    assert task.title == 'Test Task'
    assert task.description == 'Task Description'
    assert task.project == project
    assert task.assignee == user
    assert task.status == 'Grooming'
    assert task.priority == 'Medium'

@pytest.mark.django_db
def test_comment_creation():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user)
    task = Task.objects.create(title='Test Task', description='Task Description', project=project, assignee=user)
    comment = Comment.objects.create(task=task, content='This is a comment.', user=user)
    assert comment.content == 'This is a comment.'
    assert comment.task == task
    assert comment.user == user

@pytest.mark.django_db
def test_custom_user_creation():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com', role='developer')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.role == 'developer'
    assert user.avatar == 'default_avatar.png'