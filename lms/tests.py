from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            author=self.user
        )

    def test_create_lesson(self):

        data = {
            'title': 'TestCreate',
            'description': 'create_lesson',
            'course': self.course.id,
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'TestCreate', 'description': 'create_lesson', 'image_preview': None, 'video_url': None,
             'course': 1, 'author': 1}
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):

        Lesson.objects.create(
            title='TestList',
            description='list_lessons',
            course=self.course,
        )

        response = self.client.get(
            '/lesson/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['results'],
            [{'id': 1, 'title': 'TestList', 'description': 'list_lessons', 'image_preview': None, 'video_url': None,
              'course': 1, 'author': None}]
        )

    def test_retrieve_lesson(self):

        Lesson.objects.create(
            title='TestRetrieve',
            description='retrieve_lessons',
            course=self.course,
        )

        response = self.client.get(
            '/lesson/1/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'TestRetrieve', 'description': 'retrieve_lessons', 'image_preview': None,
             'video_url': None, 'course': 1, 'author': None}
        )

    def test_update_lesson(self):
        Lesson.objects.create(
            title='TestUpdate',
            description='update_lessons',
            course=self.course,
        )
        data = {
            'title': 'TestUpdated',
            'description': 'updated_lessons',
        }
        response = self.client.patch(
            '/lesson/update/1/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'TestUpdated', 'description': 'updated_lessons', 'image_preview': None,
             'video_url': None, 'course': 1, 'author': None}
        )

    def test_destroy_lesson(self):
        Lesson.objects.create(
            title='TestDestroy',
            description='update_destroy',
            course=self.course,
        )
        response = self.client.delete(
            '/lesson/destroy/1/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Subscription.objects.all().delete()


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            author=self.user
        )

    def test_create_subscription(self):
        data = {
            'course': self.course.id,
        }
        response = self.client.post(
            '/subscription/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'subscriber': 1, 'course': 1}
        )
        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_destroy_subscription(self):
        Subscription.objects.create(
            course=self.course,
        )
        response = self.client.delete(
            '/subscription/1/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Subscription.objects.all().delete()
        self.reset_sequences()


