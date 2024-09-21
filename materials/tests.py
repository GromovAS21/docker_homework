from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class Test:
    """
    Образец для создания тестовой базы данных
    """

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(course=self.course, title="Test Lesson", description="Test Description",
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)


class CourseTest(Test, APITestCase):
    """
    Тесты для модели Course
    """

    def test_retrieve_course(self):
        """
        Тест получения курса по ID
        """

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data["title"],
            "Test Course"
        )

    def test_course_create(self):
        """
        Тест создания нового курса
        """

        url = reverse("materials:course-list")
        data = {
            "title": "Test Course1",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(),
            2
        )

    def test_course_update(self):
        """
        Тест изменения курса
        """

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "title": "Test_Course2"
        }
        response = self.client.patch(url, data)
        result = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            result["title"],
            "Test_Course2"
        )

    def test_course_delete(self):
        """
        Тест удаления курса
        """

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.count(),
            0
        )

    def test_course_list(self):
        """
        Тест получения списка курсов
        """

        url = reverse("materials:course-list")
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "count_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "url_video": None,
                            "title": "Test Lesson",
                            "description": "Test Description",
                            "image": None,
                            "course": self.lesson.course.pk,
                            "owner": self.user.pk
                        },

                    ],
                    "status_subscribed": False,
                    "title": "Test Course",
                    "description": "Test Description",
                    "image": None,
                    "owner": self.user.pk
                }
            ]
        }
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            result
        )


class LessonTest(Test, APITestCase):
    """
    Тесты для модели Lesson
    """

    def test_lesson_retrieve(self):
        """
        Тест получения урока по ID
        """

        url = reverse("materials:lesson_view", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data["title"],
            "Test Lesson"
        )

    def test_lesson_create(self):
        """
        Тест создания нового урока
        """
        url = reverse("materials:lesson_create")
        data = {
            "title": "test_lesson1",
            "url_video": "https://www.youtube.com/"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_lesson_update(self):
        """
        Тест изменения урока
        """

        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "test_Lesson1"
        }
        response = self.client.patch(url, data)
        result = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            result["title"],
            "test_Lesson1"
        )

    def test_lesson_delete(self):
        """
        Тест удаления урока
        """

        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.count(),
            0
        )

    def test_lesson_list(self):
        """
        Тест получения списка уроков
        """

        url = reverse("materials:lesson_list")
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "url_video": None,
                    "title": "Test Lesson",
                    "description": "Test Description",
                    "image": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            result
        )


class SubscriptionTest(Test, APITestCase):
    """
    Тесты для модели Subscription
    """

    def test_subscription(self):
        """
        Тест подписки на курс
        """

        url = reverse("materials:subscription")

        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()["message"],
            "Подписка оформлена"
        )
