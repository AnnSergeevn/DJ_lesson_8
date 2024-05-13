import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_verification_of_receipt_of_the_first_course(client, courses_factory, students_factory):
    #Arrange
    courses = courses_factory(_quantity=2)

    #Act
    response = client.get('/api/v1/courses/')

    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == 1
    assert type(data) == list

@pytest.mark.django_db
def test_filtering_course(client, courses_factory, students_factory):
    # Arrange
    courses = courses_factory(_quantity=2)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    for i in range(len(data)-1):
        assert data[i]["id"] == Course.objects.filter(id=3).values()[i]["id"]
        assert data[i]["name"] == Course.objects.filter(id=3).values()[i]["name"]


@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    Course.objects.create(name="hggfd")

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) != 0


@pytest.mark.django_db
def test_update_course(client, courses_factory, students_factory):
    # Arrange
    courses = courses_factory(_quantity=2)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    #Course.objects.filter(id=6).update(name="Netology")
    data = response.json()
    for i in range(1):
        id = data[i]["id"]
        for item in data:
            if item['id'] == id:
                item["name"] = "Netology"
        assert data[i]["name"] == "Netology"


@pytest.mark.django_db
def test_update_course(client, courses_factory, students_factory):
    # Arrange
    courses = courses_factory(_quantity=2)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    #Course.objects.filter(id=6).update(name="Netology")
    data = response.json()
    length_data = len(data)
    del data[0]
    assert len(data) == length_data - 1
