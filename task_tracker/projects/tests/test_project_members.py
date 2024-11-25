import pytest
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

@pytest.mark.django_db
def test_add_member_to_project():
    owner = User.objects.create_user(username='owner', password='ownerpassword', email='owner@example.com')
    member = User.objects.create_user(username='member', password='memberpassword', email='member@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=owner)
    project.members.add(member)
    assert project.members.count() == 1
    assert project.members.first() == member

@pytest.mark.django_db
def test_remove_member_from_project():
    owner = User.objects.create_user(username='owner', password='ownerpassword', email='owner@example.com')
    member = User.objects.create_user(username='member', password='memberpassword', email='member@example.com')
    project = Project.objects.create(name='Test Project', description='Project Description', owner=owner)
    project.members.add(member)
    project.members.remove(member)
    assert project.members.count() == 0
