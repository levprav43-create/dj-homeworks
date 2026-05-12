import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    """Фикстура для API клиента DRF"""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фабрика для создания курсов"""
    def func(**kwargs):
        return baker.make(Course, **kwargs)
    return func


@pytest.fixture
def student_factory():
    """Фабрика для создания студентов"""
    def func(**kwargs):
        return baker.make(Student, **kwargs)
    return func