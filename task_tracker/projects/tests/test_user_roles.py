import pytest
from django.contrib.auth import get_user_model
from projects.models import Project
from user.models import CustomUser

User = get_user_model()

@pytest.mark.django_db
def test_user_role_assignment():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com', role='tester')
    assert user.role == 'tester'

@pytest.mark.django_db
def test_user_current_projects():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user)
    user.current_projects.add(project)
    assert user.current_projects.count() == 1
    assert user.current_projects.first() == project

@pytest.mark.django_db
def test_user_project_history():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=user)
    user.project_history.add(project)
    assert user.project_history.count() == 1
    assert user.project_history.first() == project
