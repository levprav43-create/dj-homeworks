import pytest
from django.urls import reverse
from rest_framework import status
from model_bakery import baker

from students.models import Course


@pytest.mark.django_db
class TestCoursesAPI:
    """Тесты для API курсов"""

    # 1. Проверка получения первого курса (retrieve)
    def test_retrieve_course(self, api_client, course_factory):
        course = course_factory(name="Python Basic")
        url = reverse("courses-detail", kwargs={"pk": course.id})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == course.name

    # 2. Проверка получения списка курсов (list)
    def test_list_courses(self, api_client, course_factory):
        course_factory(name="Course 1")
        course_factory(name="Course 2")
        url = reverse("courses-list")
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    # 3. Проверка фильтрации списка курсов по id
    def test_filter_by_id(self, api_client, course_factory):
        course1 = course_factory(name="Course 1")
        course_factory(name="Course 2")
        url = reverse("courses-list")
        
        response = api_client.get(url, data={"id": course1.id})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == course1.id

    # 4. Проверка фильтрации списка курсов по name (ТОЧНОЕ СОВПАДЕНИЕ!)
    def test_filter_by_name(self, api_client, course_factory):
        """Фильтрация по name работает как точное совпадение (не поиск по подстроке)"""
        # Arrange: создаём курсы, один с точным именем "Python"
        course_factory(name="Python")  # ← точное имя для фильтра
        course_factory(name="Python Basic")
        course_factory(name="Django Pro")
        url = reverse("courses-list")
        
        # Act: делаем запрос с фильтром по точному имени
        response = api_client.get(url, data={"name": "Python"})
        
        # Assert: должен вернуться только курс с именем "Python"
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Python"

    # 5. Тест успешного создания курса
    def test_create_course(self, api_client):
        url = reverse("courses-list")
        data = {"name": "New Course via API"}
        
        response = api_client.post(url, data=data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.filter(name="New Course via API").exists()

    # 6. Тест успешного обновления курса
    def test_update_course(self, api_client, course_factory):
        course = course_factory(name="Old Name")
        url = reverse("courses-detail", kwargs={"pk": course.id})
        data = {"name": "Updated Name"}
        
        response = api_client.patch(url, data=data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        course.refresh_from_db()
        assert course.name == "Updated Name"

    # 7. Тест успешного удаления курса
    def test_delete_course(self, api_client, course_factory):
        course = course_factory(name="To Delete")
        url = reverse("courses-detail", kwargs={"pk": course.id})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Course.objects.filter(id=course.id).exists()